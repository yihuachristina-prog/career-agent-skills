#!/usr/bin/env python3
"""Validate one run's seven-source coverage manifest."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from urllib.parse import urlsplit, urlunsplit
from pathlib import Path


EXPECTED_SOURCES = ["脉脉", "猎聘", "BOSS直聘", "51job", "智联招聘", "LinkedIn", "企业官网"]
ALLOWED_MODES = {"active", "unattended"}
ALLOWED_STATUSES = {"已登录深扫", "部分完成", "公开搜索", "登录待刷新", "页面受限", "无结果"}


def canonical_url(value: str) -> str:
    """Only drop known tracking keys; job IDs in query strings remain significant."""
    from urllib.parse import parse_qsl, urlencode, unquote
    u = urlsplit(value or "")
    if not u.scheme: return value or ""
    query = [(k,v) for k,v in parse_qsl(u.query) if not k.lower().startswith('utm_') and k.lower() not in {'trackingid','refid','trk'}]
    return urlunsplit((u.scheme,u.netloc.lower(),unquote(u.path).rstrip('/'),urlencode(query),''))


def reconcile_observation(current: dict, observation: dict) -> dict:
    """Pure proposed patch for an already identity-matched job; never writes a ledger.

    Identity must be an exact platform ID/URL or an evidenced cross-platform link.
    Absence of evidence is not a closure, user decision, or re-open instruction.
    """
    result = deepcopy(current)
    current_id = current.get('岗位编号')
    if not current_id or observation.get('岗位编号') != current_id:
        raise ValueError('岗位编号不一致，不允许跨岗位覆盖')
    links = [current.get('原始链接',''), *current.get('关联来源', [])]
    match = canonical_url(observation.get('url','')) in {canonical_url(x) for x in links if x}
    if not match and not observation.get('same_job_evidence'):
        raise ValueError('新来源未证明为同一岗位，应待核验关联')
    result['关联来源'] = list(dict.fromkeys(x for x in [*current.get('关联来源',[]),observation.get('url')] if x))
    outcome = observation.get('outcome')
    if outcome not in {'source_failed','jd_incomplete','closed','readable'}:
        raise ValueError('未识别的读取结果，不允许推定岗位状态')
    result['本轮读取结果'] = outcome
    result['new_opportunity'] = False
    result['notify'] = False
    if outcome in {'source_failed','jd_incomplete'}:
        result['本轮缺项'] = observation.get('missing', '同岗位页面正文')
        return result
    state = current.get('状态','')
    protected = any(x in state for x in ('已投递','HR','面试','已结束','已失效','不投','跳过','放弃'))
    if outcome == 'closed':
        if not observation.get('closure_evidence'):
            raise ValueError('关闭结论缺少同岗明确证据')
        result['招聘在线状态'] = '明确关闭'
        if not protected: result['状态'] = '已失效'
        return result
    if observation.get('material_change'):
        result['本轮实质变化'] = observation['material_change']
        result['notify'] = not any(x in state for x in ('已投递','HR','面试'))
    if outcome == 'readable':
        if observation.get('jd'):
            result['完整JD/快照'] = observation['jd']
        if observation.get('open_evidence'):
            result['招聘在线状态'] = '公开页可投递'
    # The original decision/state always survives a repeat hit. Reassessment after
    # a material change is a separate existing skill action, never an implicit reset.
    return result


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("mode") not in ALLOWED_MODES:
        errors.append("mode 必须为 active 或 unattended")

    rows = data.get("sources")
    if not isinstance(rows, list):
        return errors + ["sources 必须为数组"]

    names = [row.get("source") for row in rows if isinstance(row, dict)]
    missing = [name for name in EXPECTED_SOURCES if name not in names]
    extra = [name for name in names if name not in EXPECTED_SOURCES]
    if missing:
        errors.append("缺少来源: " + ", ".join(missing))
    if extra:
        errors.append("存在范围外来源: " + ", ".join(map(str, extra)))
    if len(names) != len(set(names)):
        errors.append("来源记录重复")

    for row in rows:
        if not isinstance(row, dict):
            errors.append("来源记录必须为对象")
            continue
        name = row.get("source", "未知来源")
        status = row.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{name}: 非法覆盖状态 {status!r}")
        visible = row.get("favorites_visible", 0)
        checked = row.get("favorites_checked", 0)
        if not isinstance(visible, int) or not isinstance(checked, int) or visible < 0 or checked < 0:
            errors.append(f"{name}: 收藏数量必须为非负整数")
            continue
        if checked > visible:
            errors.append(f"{name}: 已复核收藏数不能大于可见收藏数")
        if status == "已登录深扫" and checked != visible:
            errors.append(f"{name}: 登录态深扫未复核全部可见收藏")
        if status == "部分完成" and checked >= visible and row.get("pagination_complete", False):
            errors.append(f"{name}: 已完成全部收藏时不应标记部分完成")
        if status == "无结果" and not row.get("search_completed", False):
            errors.append(f"{name}: 未完成搜索不能写无结果")
        if status == "无结果" and row.get("read_error"):
            errors.append(f"{name}: 来源读取失败不能写无结果")

    mutations = data.get("external_mutations", [])
    if mutations:
        errors.append("检测到招聘平台外部写操作: " + ", ".join(map(str, mutations)))
    # Optional proposals reuse the run manifest, rather than adding another tracker.
    for update in data.get('updates', []):
        try:
            expected = reconcile_observation(update['before'],update['observation'])
            for key in ('岗位编号','状态','new_opportunity','招聘在线状态'):
                if key in update.get('after', {}) and update['after'][key] != expected.get(key):
                    errors.append(f"{update['before'].get('岗位编号')}:写回将误改{key}")
        except (KeyError,ValueError,TypeError) as exc:
            errors.append('岗位连续性核验失败:'+str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate(data)
    print(json.dumps({"valid": not errors, "errors": errors, "source_count": len(data.get("sources", []))}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
