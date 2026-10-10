#!/usr/bin/env python3
"""Plan and apply exact deletion of terminal gray-job material directories.

The caller must first validate gray fill, terminal status, ledger fields, and
asset-index rows from the shared workbooks. This helper only accepts exact job
IDs and refuses paths that are not direct children of the configured package
root. `plan` is non-destructive; `apply` revalidates the manifest before each
deletion and continues past per-job failures.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
from typing import Any


JOB_ID_RE = re.compile(r"^[A-Z]{2,3}-(?:[0-9]{3}|[0-9]{8}-[A-Za-z0-9]+)$")
SCHEMA_VERSION = 2



def native_path(path: Path) -> Path:
    if os.name != "nt":
        return path
    text = str(path.absolute())
    if text.startswith("\\\\?\\"):
        return Path(text)
    if text.startswith("\\\\"):
        return Path("\\\\?\\UNC\\" + text[2:])
    return Path("\\\\?\\" + text)


def display_path(path: Path) -> Path:
    text = str(path)
    if text.startswith("\\\\?\\UNC\\"):
        text = "\\\\" + text[8:]
    elif text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text)


def canonical_path(path: Path, strict: bool = False) -> Path:
    return display_path(native_path(path).resolve(strict=strict))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with native_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_reparse_point(path: Path) -> bool:
    info = native_path(path).lstat()
    attributes = getattr(info, "st_file_attributes", 0)
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def validate_root(raw_root: str) -> Path:
    literal_root = Path(raw_root).absolute()
    if is_reparse_point(literal_root):
        raise ValueError("package root cannot be a reparse point")
    root = canonical_path(literal_root, strict=True)
    if not native_path(root).is_dir():
        raise ValueError(f"package root is not a directory: {root}")
    if is_reparse_point(root):
        raise ValueError(f"package root cannot be a reparse point: {root}")
    return root


def validate_target(root: Path, job_id: str) -> Path:
    if not JOB_ID_RE.fullmatch(job_id):
        raise ValueError(f"invalid job id: {job_id!r}")
    candidates = [display_path(p) for p in native_path(root).iterdir() if p.name == job_id or p.name.split("_", 1)[0] == job_id]
    if len(candidates) > 1:
        raise ValueError("multiple directories for exact job id; reconcile first")
    literal = candidates[0] if candidates else root / job_id
    if native_path(literal).exists() and is_reparse_point(literal):
        raise ValueError("target cannot be a reparse point")
    resolved = canonical_path(literal)
    if resolved.parent != root or resolved.name.split("_", 1)[0] != job_id:
        raise ValueError(f"target is not an exact direct child of package root: {literal}")
    return literal


def snapshot_target(root: Path, job_id: str) -> dict[str, Any]:
    target = validate_target(root, job_id)
    if not native_path(target).exists():
        return {
            "job_id": job_id,
            "directory": str(target),
            "exists": False,
            "file_count": 0,
            "files": [],
        }
    if not native_path(target).is_dir() or is_reparse_point(target):
        raise ValueError(f"target must be a normal directory: {target}")

    files: list[dict[str, Any]] = []
    for current, dirs, names in os.walk(native_path(target), topdown=True, followlinks=False):
        current_path = display_path(Path(current))
        for directory in dirs:
            child = current_path / directory
            if is_reparse_point(child):
                raise ValueError(f"reparse point found inside target: {child}")
        for name in names:
            child = current_path / name
            if is_reparse_point(child):
                raise ValueError(f"reparse point found inside target: {child}")
            files.append(
                {
                    "path": child.relative_to(target).as_posix(),
                    "size": native_path(child).stat().st_size,
                    "sha256": sha256_file(child),
                }
            )
    files.sort(key=lambda item: item["path"])
    return {
        "job_id": job_id,
        "directory": str(target),
        "exists": True,
        "file_count": len(files),
        "files": files,
    }


def build_manifest(root: Path, job_ids: list[str]) -> dict[str, Any]:
    unique_ids = list(dict.fromkeys(job_ids))
    if not unique_ids:
        raise ValueError("at least one --job-id is required")
    return {
        "schema_version": SCHEMA_VERSION,
        "packages_root": str(root),
        "targets": [snapshot_target(root, job_id) for job_id in unique_ids],
    }


def same_snapshot(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    keys = ("job_id", "directory", "exists", "file_count", "files")
    return all(expected.get(key) == actual.get(key) for key in keys)


def apply_manifest(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported manifest schema_version")
    if canonical_path(Path(str(manifest.get("packages_root"))), strict=True) != root:
        raise ValueError("manifest package root does not match --packages-root")

    results = []
    for expected in manifest.get("targets", []):
        job_id = str(expected.get("job_id", ""))
        try:
            actual = snapshot_target(root, job_id)
            if not same_snapshot(expected, actual):
                raise ValueError("directory contents changed after planning")
            if actual["exists"]:
                shutil.rmtree(native_path(validate_target(root, job_id)))
                if native_path(validate_target(root, job_id)).exists():
                    raise RuntimeError("directory still exists after deletion")
                outcome = "deleted"
            else:
                outcome = "already_absent"
            results.append(
                {
                    "job_id": job_id,
                    "status": outcome,
                    "file_count": actual["file_count"],
                }
            )
        except Exception as exc:  # continue other exact job targets
            results.append({"job_id": job_id, "status": "blocked", "error": str(exc)})
    return {
        "schema_version": SCHEMA_VERSION,
        "packages_root": str(root),
        "results": results,
        "all_succeeded": all(item["status"] != "blocked" for item in results),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="create a non-destructive manifest")
    plan_parser.add_argument("--packages-root", required=True)
    plan_parser.add_argument("--job-id", action="append", required=True)
    plan_parser.add_argument("--output")

    apply_parser = subparsers.add_parser("apply", help="revalidate and delete manifest targets")
    apply_parser.add_argument("--packages-root", required=True)
    apply_parser.add_argument("--manifest", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = validate_root(args.packages_root)
        if args.command == "plan":
            payload = build_manifest(root, args.job_id)
            text = json.dumps(payload, ensure_ascii=False, indent=2)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            print(text)
            return 0

        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        payload = apply_manifest(root, manifest)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["all_succeeded"] else 2
    except Exception as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
