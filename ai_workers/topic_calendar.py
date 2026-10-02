"""📅 주제 캘린더 — 이번 달에 쓸 글감.

Naver's C-Rank rewards a blog that covers one subject *consistently*; a blog
with six posts, the last one two years old, has nothing for it to measure.
For a blog in that state, publishing steadily on topic matters more than
optimizing any single post — and the step that stalls a busy staffer is not
writing (the pipeline does that) but deciding what to write about this week.

The topics themselves live in core/brand_seed.TOPIC_CALENDAR (they are the
company's, like the rest of the Brand Kit); this module only picks which ones
to suggest now.
"""
from __future__ import annotations

from datetime import date
from typing import List

from core import brand_seed

# 이번 달 주제 외에 함께 보여줄 상시 주제 수.
EVERGREEN_SUGGESTIONS = 3


def suggestions(today: date | None = None, used: set | None = None) -> dict:
    """{"this_month": [...], "next_month": [...], "evergreen": [...]}, unused first.

    Next month is shown because seasonal posts need lead time: a 추석 대청소
    post published the week of 추석 is read by nobody who could still book.
    """
    today = today or date.today()
    used = used or set()
    this_month = today.month
    next_month = this_month % 12 + 1

    # 기본 화자(주간보호·방문요양) 주제가 먼저 — SNS 강화의 대상 사업입니다. 그다음 안 쓴 주제 순.
    from ai_workers import post_types

    def rank(t: dict):
        return (post_types.voice_of(t.get("post_type")) == "house", t["title"] in used)

    def pick(month: int) -> List[dict]:
        rows = [t for t in brand_seed.TOPIC_CALENDAR if t["month"] == month]
        return sorted(rows, key=rank)

    evergreen = sorted(
        [t for t in brand_seed.TOPIC_CALENDAR if t["month"] == 0 and t["title"] not in used], key=rank
    )
    return {
        "this_month": pick(this_month),
        "next_month": pick(next_month),
        "evergreen": evergreen[:EVERGREEN_SUGGESTIONS],
        "month": this_month,
        "next": next_month,
    }
