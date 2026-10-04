"""당근 비즈프로필 '소식' writer — the fifth channel, and the local one.

A home-service provider's customers are, by definition, within a few
kilometres of it. Naver blog search finds people who already know what to
type; Instagram reaches whoever follows the account. 당근 reaches the
neighbourhood itself: its 비즈프로필 소식 is shown to residents near the
business, which for a 강서구·양천구 service is exactly the market.

The shape differs from every other channel here, so it gets its own writer
rather than a shortened blog post:

- read as a neighbour's notice, not an ad — plain, specific, no hook tricks
- no hashtags (소식 is not discovered by tag; see sns_validator.validate_daangn)
- the neighbourhood is named when the post is about one, never invented
- one concrete next step: a phone number or the online application

Best-effort and audited, exactly like the Instagram caption (see
content_writer._guarded_daangn).
"""
from __future__ import annotations

from typing import List

from ai_workers.multi_llm_router import generate_text, parse_json_object
from ai_workers.prompt_builder import brand_voice_blocks

DAANGN_SYSTEM_PROMPT_BASE = (
    "당신은 동네 가게·기관의 당근(당근마켓) 비즈프로필 '소식'을 쓰는 담당자입니다. 소식은 "
    "가까운 동네 주민의 피드에 뜨므로, 광고 문구가 아니라 이웃에게 알리는 안내문처럼 씁니다.\n"
    "- 제목은 30자 이내로, 무엇에 관한 소식인지 바로 알 수 있게 씁니다. 낚시성 표현과 느낌표 "
    "남발은 쓰지 않습니다.\n"
    "- 본문은 200~500자. 첫 문장은 동네 이웃의 생활 장면이나 이 소식의 핵심으로 시작합니다.\n"
    "- 무엇을, 누구에게, 얼마에(확정된 금액만), 어떻게 신청하는지를 짧은 문단으로 담습니다.\n"
    "- 자료에 나온 동네 이름은 써도 되지만, 자료에 없는 동네·아파트 이름을 지어내지 마세요.\n"
    "- 해시태그는 쓰지 않습니다.\n"
    "- 마지막 문단은 전화 문의나 온라인 신청처럼 바로 할 수 있는 행동 하나로 끝냅니다.\n"
    "반드시 아래 JSON 형식으로만 응답하고 다른 설명은 포함하지 마세요:\n"
    '{"title": "소식 제목", "body": "소식 본문"}'
)


def build_system_prompt(brand_kit: dict) -> str:
    parts = [DAANGN_SYSTEM_PROMPT_BASE] + brand_voice_blocks(brand_kit)
    areas = brand_kit.get("service_areas") or []
    if areas:
        parts.append("[서비스 지역] " + ", ".join(areas) + " — 이 범위 밖의 지역을 서비스한다고 쓰지 마세요.")
    return "\n\n".join(parts)


def _parse_response(raw: str, fallback_text: str) -> dict:
    try:
        parsed = parse_json_object(raw)
        return {
            "title": str(parsed.get("title") or "").strip(),
            "body": str(parsed.get("body") or fallback_text).strip(),
        }
    except Exception:
        return {"title": "", "body": fallback_text}


def write_daangn_post(
    note: str, photo_captions: List[str], brand_kit: dict, vendor: str, facts: str = ""
) -> dict:
    """Returns {"title": str, "body": str}. Best-effort, like the other SNS writers.

    `facts` is the same confirmed-facts block + audited blog body the other
    writers get (content_writer._sns_facts), so prices and dates agree.
    """
    context = "\n".join(f"- {c}" for c in photo_captions) if photo_captions else "(첨부된 사진 없음)"
    prompt = f"[담당자가 작성한 메모]\n{note}\n\n[첨부 사진 설명]\n{context}"
    if facts:
        prompt += "\n\n" + facts
    raw = generate_text(
        vendor=vendor,
        prompt=prompt,
        system=build_system_prompt(brand_kit),
        max_tokens=900,
        note="daangn-post",
    )
    return _parse_response(raw, note)
