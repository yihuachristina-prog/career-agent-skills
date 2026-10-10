#!/usr/bin/env python3
"""Normalize common Chinese recruitment salary strings to annual RMB ranges."""

from __future__ import annotations

import argparse
import json
import re

DEFAULT_CURRENT_ANNUAL_RMB = None
DEFAULT_CURRENT_MONTHLY_BASE_RMB = None
DEFAULT_OFFER_FLOOR_RMB = None
DEFAULT_LISTING_MAX_FLOOR_RMB = None
DEFAULT_LISTING_MIN_PREFERENCE_RMB = None
MAX_RANGE_RATIO = 1.6


def assess_range(result: dict, profile: dict) -> dict:
    low = result["annual_min_rmb"]
    high = result["annual_max_rmb"]
    current_annual = profile["current_annual_rmb"]
    current_monthly_base = profile["current_monthly_base_rmb"]
    listing_max_floor = profile["listing_max_floor_rmb"]
    listing_min_preference = profile["listing_min_preference_rmb"]

    assessment = {
        **profile,
        "monthly_base_judgment": "月 Base 待核实",
        "range_midpoint_rmb": None,
        "range_ratio": None,
        "current_position": "待核实",
        "salary_judgment": "待核实",
        "default_action": "verify",
    }
    monthly_low = result.get("monthly_min_rmb")
    monthly_high = result.get("monthly_max_rmb")
    if monthly_high is not None:
        if monthly_high < current_monthly_base:
            assessment["monthly_base_judgment"] = "上限不足"
        elif monthly_low is not None and monthly_low < current_monthly_base:
            assessment["monthly_base_judgment"] = "实际定薪待核实"
        else:
            assessment["monthly_base_judgment"] = "达标"

    # 月 Base 与年包分别判断；未披露薪数不默认按 12 薪补齐。
    if monthly_high is not None and monthly_high < current_monthly_base:
        assessment["salary_judgment"] = "月 Base 上限不足"
        assessment["default_action"] = "exclude"
        return assessment
    if low is None or high is None:
        assessment["salary_judgment"] = "年包及发薪月数待核实" if monthly_high is not None else "待核实"
        return assessment

    assessment["range_midpoint_rmb"] = round((low + high) / 2)
    assessment["range_ratio"] = round(high / low, 3) if low > 0 else None

    if high == low:
        assessment["current_position"] = (
            "低于区间" if current_annual < low else "等于/高于上限"
        )
    elif current_annual < low:
        assessment["current_position"] = "低于区间"
    elif current_annual >= high:
        assessment["current_position"] = "等于/高于上限"
    else:
        percentile = (current_annual - low) / (high - low)
        assessment["current_position_percentile"] = round(percentile, 3)
        if percentile < 1 / 3:
            assessment["current_position"] = "区间下段"
        elif percentile <= 2 / 3:
            assessment["current_position"] = "区间中部"
        else:
            assessment["current_position"] = "区间上段"

    if monthly_high is not None and monthly_high < current_monthly_base:
        assessment["salary_judgment"] = "月 Base 上限不足"
        assessment["default_action"] = "exclude"
    elif high < listing_max_floor:
        assessment["salary_judgment"] = "年包上限不足"
        assessment["default_action"] = "exclude"
    elif low < listing_min_preference:
        assessment["salary_judgment"] = "年包下限偏低"
        assessment["default_action"] = (
            "verify" if result["confidence"] != "high" else "exclude"
        )
    elif (
        monthly_low is not None
        and monthly_high is not None
        and monthly_low < current_monthly_base <= monthly_high
    ):
        assessment["salary_judgment"] = "实际月 Base 待核实"
        assessment["default_action"] = "verify"
    elif monthly_low is None or monthly_high is None:
        assessment["salary_judgment"] = "月 Base 待核实"
        assessment["default_action"] = "verify"
    elif assessment["range_ratio"] and assessment["range_ratio"] > MAX_RANGE_RATIO:
        assessment["salary_judgment"] = "区间过宽"
        assessment["default_action"] = "verify"
    elif assessment["current_position"] in {"区间上段", "等于/高于上限"}:
        assessment["salary_judgment"] = "可能达标"
        assessment["default_action"] = "verify"
    else:
        assessment["salary_judgment"] = "结构达标"
        assessment["default_action"] = "keep"

    return assessment


def normalize(text: str, profile: dict | None = None) -> dict:
    profile = profile or default_profile()
    raw = text.strip()
    compact = raw.replace(" ", "").replace(",", "")

    annual = re.fullmatch(r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)万/年", compact, re.I)
    if annual:
        low, high = map(float, annual.groups())
        result = {
            "raw": raw,
            "annual_min_rmb": round(low * 10000),
            "annual_max_rmb": round(high * 10000),
            "monthly_min_rmb": None,
            "monthly_max_rmb": None,
            "months": None,
            "confidence": "high",
            "basis": "annual",
        }
        result.update(assess_range(result, profile))
        return result

    monthly = re.fullmatch(
        r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)([kK千万])(?:/月)?(?:[·xX×](\d+)薪)?",
        compact,
    )
    if monthly:
        low, high, unit, months_text = monthly.groups()
        factor = 10000 if unit == "万" else 1000
        months = int(months_text) if months_text else None
        result = {
            "raw": raw,
            "annual_min_rmb": round(float(low) * factor * months) if months else None,
            "annual_max_rmb": round(float(high) * factor * months) if months else None,
            "monthly_min_rmb": round(float(low) * factor),
            "monthly_max_rmb": round(float(high) * factor),
            "months": months,
            "confidence": "high" if months_text else "low",
            "basis": "monthly",
        }
        result.update(assess_range(result, profile))
        return result

    result = {
        "raw": raw,
        "annual_min_rmb": None,
        "annual_max_rmb": None,
        "monthly_min_rmb": None,
        "monthly_max_rmb": None,
        "months": None,
        "confidence": "unknown",
        "basis": "unparsed",
    }
    result.update(assess_range(result, profile))
    return result


def default_profile() -> dict:
    raise ValueError("Salary thresholds are required for the current user; pass an explicit profile.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize a Chinese recruitment salary string."
    )
    parser.add_argument("salary_text")
    parser.add_argument(
        "--current-annual",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--current-monthly-base",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--offer-floor",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--listing-max-floor",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--listing-min-preference",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    profile = {
        "current_annual_rmb": args.current_annual,
        "current_monthly_base_rmb": args.current_monthly_base,
        "offer_floor_rmb": args.offer_floor,
        "listing_max_floor_rmb": args.listing_max_floor,
        "listing_min_preference_rmb": args.listing_min_preference,
    }
    print(json.dumps(normalize(args.salary_text, profile), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
