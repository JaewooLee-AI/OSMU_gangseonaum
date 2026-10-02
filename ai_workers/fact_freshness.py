"""Brand Kit numbers that carry a year — are they still this year's?

Prices, voucher amounts and staff counts in the Brand Kit are stated "2026년
기준". They are injected as the *only* numbers the model may use, and the
compliance audit treats them as ground truth — so on 1 January the app keeps
publishing last year's price list, and the audit will even "correct" a new
price back to the old one. Nothing fails; it is simply wrong.

This module only reports. Updating a price is a fact only the company can
supply, so the fix is a warning that says which lines to re-check.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Dict, List

_YEAR_RE = re.compile(r"(20\d{2})년")
# 해마다 바뀌는 종류의 사실 — 금액·요금·인원·한도.
_YEARLY_RE = re.compile(r"요금|원|바우처|한도|기준|명")

# 12월에는 다음 해 요금표를 미리 확인하라고 알립니다.
ADVANCE_NOTICE_MONTH = 12


def check(brand_kit: dict, today: date | None = None) -> Dict[str, object]:
    today = today or date.today()
    sources = [("핵심 팩트", f) for f in brand_kit.get("core_facts") or []]
    sources += [("예시 글", s) for s in brand_kit.get("few_shot_samples") or []]
    sources += [("서비스 기본값", v) for v in (brand_kit.get("product_defaults") or {}).values()]

    stale: List[dict] = []
    upcoming: List[dict] = []
    for where, text in sources:
        text = str(text)
        if not _YEARLY_RE.search(text):
            continue
        years = [int(y) for y in _YEAR_RE.findall(text)]
        if not years:
            continue
        newest = max(years)
        item = {"where": where, "year": newest, "text": text[:80] + ("…" if len(text) > 80 else "")}
        if newest < today.year:
            stale.append(item)
        elif newest == today.year and today.month >= ADVANCE_NOTICE_MONTH:
            upcoming.append(item)
    return {"stale": stale, "upcoming": upcoming, "year": today.year}


def summary(brand_kit: dict, today: date | None = None) -> str:
    """One line for a banner, or '' when nothing needs attention."""
    result = check(brand_kit, today)
    if result["stale"]:
        years = sorted({i["year"] for i in result["stale"]})
        return (
            f"📅 브랜드 킷에 {', '.join(map(str, years))}년 기준 요금·수치가 {len(result['stale'])}곳 있습니다. "
            f"{result['year']}년 요금표가 나왔다면 핵심 팩트·예시 글·서비스 기본값을 함께 고쳐 주세요 — "
            "이 숫자가 모든 글과 컴플라이언스 검수의 기준입니다."
        )
    if result["upcoming"]:
        return (
            f"📅 곧 {result['year'] + 1}년입니다. 새 요금표·지원 제도 기준이 나오면 브랜드 킷의 "
            f"{result['year']}년 기준 수치 {len(result['upcoming'])}곳을 바꿔야 합니다."
        )
    return ""
