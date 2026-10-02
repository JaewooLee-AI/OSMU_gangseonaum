"""글 유형 — 워크벤치에서 한 번 고르면 모드·시트·메모 틀이 함께 정해집니다.

The workbench asks a care-center staffer for a content mode (3 choices), two
fact sheets (16 fields) and a memo before anything is generated. Each of
those choices is reasonable on its own; together they are a form most people
fill in the same way for the same kind of post. A post type is that shared
answer, applied in one click and still editable afterwards.

Nothing here changes how generation works. Applying a type only pre-fills
inputs the pipeline already reads — the mode radio, the 🧹 서비스·이용 정보
fields (from the Brand Kit's `product_defaults`, never invented), and a memo
skeleton — so a post generated after picking a type is exactly the post the
same inputs would have produced by hand.
"""
from __future__ import annotations

from typing import Dict, List

# key -> definition. `defaults` lists which Brand Kit product_defaults keys
# this kind of post must carry: a 요금 안내 has to state the price, a 생활 팁
# should not be forced to recite the whole price list ("하나도 빠뜨리지 말고"
# is how the factsheet block phrases it).
POST_TYPES: Dict[str, dict] = {
    # --- [돌봄] 주간보호·방문요양 — 기본 화자(SNS 강화의 대상 사업) ---------------------
    "care": {
        "label": "🧓 [돌봄] 주간보호·방문요양 안내",
        "mode": "seo",
        "defaults": ["moq", "size", "options", "order"],
        "defaults_source": "care",
        "voice": None,
        "open_sheet": "product",
        "memo": "이번 글에서 소개할 돌봄(주간보호/방문요양): [ ]\n보호자에게 자주 듣는 고민: [ ]\n현장 이야기: [ ]",
        "hint": "검색으로 들어온 보호자가 대상·운영 시간·송영·상담 전화를 바로 찾도록 노출 우선으로 씁니다. 건강 효과는 단정하지 않습니다.",
    },
    "care_guide": {
        "label": "📘 [돌봄] 보호자 정보 (장기요양등급·제도)",
        "mode": "seo",
        "defaults": ["order"],
        "defaults_source": "care",
        "voice": None,
        "open_sheet": None,
        "memo": "이번 글에서 설명할 제도 정보: [ ]\n보호자에게 자주 듣는 질문: [ ]",
        "hint": "브랜드 킷의 [제도 정보] 팩트(출처: 국민건강보험공단·법령)만으로 씁니다. 등급은 공단이 정하며, 센터가 대신 받아 준다고 쓰지 않습니다.",
    },
    "care_story": {
        "label": "💬 [돌봄] 센터 현장 이야기 (익명)",
        "mode": "balanced",
        "defaults": ["order"],
        "defaults_source": "care",
        "voice": None,
        "open_sheet": None,
        "memo": "프로그램·하루 일과 중 있었던 일: [ ]\n어르신·보호자 반응: [ ]\n※ 어르신 실명·얼굴이 보이는 사진은 쓰지 않습니다.",
        "hint": "실제 현장 이야기가 있어야 다른 글과 겹치지 않습니다. 사진 속 얼굴은 동의가 확인된 것만 쓰세요.",
    },
    "recruit_care": {
        "label": "🙋 [돌봄] 요양보호사 모집",
        "mode": "balanced",
        "defaults": [],
        "voice": None,
        "open_sheet": "notice",
        "memo": "모집 분야(주간보호/방문요양): [ ]\n근무 조건: [ ]",
        "hint": "📣 공지 정보에 대상·정원·신청 방법·마감·문의를 채우세요. 비운 항목은 지어내지 않습니다.",
    },
    # --- [가사] 우렁각시 홈서비스 — 보조 화자(house_voice) --------------------------
    "service": {
        "label": "🧹 [가사] 서비스·요금 안내",
        "mode": "seo",
        "defaults": ["price", "moq", "size", "options", "custom", "order"],
        "voice": "house",
        "open_sheet": "product",
        "memo": "이번 글에서 소개할 서비스: [ ]\n특히 강조할 점: [ ]",
        "hint": "검색으로 들어온 사람이 요금·범위·신청 방법을 바로 찾도록 노출 우선으로 씁니다.",
    },
    "voucher": {
        "label": "🎫 [가사] 서울형 가사서비스 안내",
        "mode": "seo",
        "defaults": ["custom", "price", "size", "order"],
        "voice": "house",
        "open_sheet": "product",
        "memo": "안내할 지원 제도: [ ]\n자주 받는 질문: [ ]",
        "hint": "지원 대상·한도·신청 창구를 정확히 담습니다. 조건을 빼고 '무료'라고 쓰지 않습니다.",
    },
    "review": {
        "label": "💬 [가사] 이용 후기 (익명)",
        "mode": "balanced",
        "defaults": ["size", "order"],
        "voice": "house",
        "open_sheet": None,
        "memo": "[동네] [가구 형태] 고객, [정기/일회성] [시간].\n요청한 일: [ ]\n해피콜·고객 반응: [ ]\n※ 실명·동호수·얼굴이 보이는 사진은 쓰지 않습니다.",
        "hint": "실제 현장 이야기가 있어야 다른 글과 겹치지 않습니다. 개인정보는 빼고 적으세요.",
    },
    "tip": {
        "label": "💡 [가사] 생활 팁 · 계절 이야기",
        "mode": "balanced",
        "defaults": ["order"],
        "voice": "house",
        "open_sheet": None,
        "memo": "다룰 생활 장면: [ ]\n가사서비스로 맡길 수 있는 부분: [ ]",
        "hint": "독자의 생활 고민으로 열고, 서비스는 필요한 만큼만 곁들입니다.",
    },
    "recruit": {
        "label": "👥 [가사] 가사관리사 모집",
        "mode": "balanced",
        "defaults": [],
        "voice": "house",
        "open_sheet": "notice",
        "memo": "모집 직무: [ ]\n지원 자격·교육: [ ]\n근무 조건: [ ]",
        "hint": "📣 공지 정보에 대상·정원·신청 방법·마감·문의를 채우세요. 비운 항목은 지어내지 않습니다.",
    },
    # --- 공통 (기본 화자) ----------------------------------------------------------
    "notice": {
        "label": "📣 공지 (휴무·일정)",
        "mode": "rich",
        "defaults": [],
        "voice": None,
        "open_sheet": "notice",
        "memo": "알릴 내용: [ ]",
        "hint": "📣 공지 정보의 해당 칸(일시 등)만 채우면 짧은 공지로 씁니다.",
    },
    "free": {
        "label": "✍️ 자유 글",
        "mode": None,  # 브랜드 킷 기본 모드
        "defaults": [],
        "voice": None,
        "open_sheet": None,
        "memo": "",
        "hint": "모드와 입력을 직접 정합니다. 화자는 기본(주간보호·방문요양)입니다.",
    },
}

ORDER: List[str] = [
    "care", "care_guide", "care_story", "recruit_care",
    "service", "voucher", "review", "tip", "recruit",
    "notice", "free",
]


def voice_of(post_type: str | None) -> str | None:
    """'house' for a 가사서비스 post, None for the default (주간보호) voice."""
    return (get(post_type) or {}).get("voice")


def get(key: str | None) -> dict | None:
    return POST_TYPES.get((key or "").strip())


def _defaults_for(spec: dict, brand_kit: dict) -> dict:
    if spec.get("defaults_source") == "care":
        from core import brand_seed
        return brand_kit.get("care_defaults") or brand_seed.CARE_PRODUCT_DEFAULTS
    return brand_kit.get("product_defaults") or {}


def _known_default_values(brand_kit: dict) -> Dict[str, set]:
    """Every default a key could have been pre-filled with, from any source —
    so switching from 서비스 안내 to 어르신 돌봄 clears the 가사 요금 the
    first type filled in, and the other way round."""
    from core import brand_seed
    known: Dict[str, set] = {}
    for source in (
        brand_kit.get("product_defaults") or {},
        brand_kit.get("care_defaults") or {},
        brand_seed.CARE_PRODUCT_DEFAULTS,
    ):
        for key, value in source.items():
            if (value or "").strip():
                known.setdefault(key, set()).add(value.strip())
    return known


def default_product_fields(post_type: str | None, brand_kit: dict, current: dict | None = None) -> dict:
    """The 🧹 서비스·이용 정보 values a post of this type should start with.

    Only fills keys that are empty in `current`, so applying a type never
    overwrites what the staffer has already typed for this post. Switching
    type also clears keys the new type doesn't carry — but only while they
    still hold the untouched Brand Kit default: picking 요금 안내 and then
    생활 팁 must not leave the tip post obliged to recite the price list,
    and a value the staffer edited is theirs either way.
    """
    spec = get(post_type)
    current = dict(current or {})
    if not spec:
        return current
    defaults = _defaults_for(spec, brand_kit)
    known = _known_default_values(brand_kit)
    for key, value in list(current.items()):
        stripped = (value or "").strip()
        if stripped and stripped in known.get(key, set()) and (
            key not in spec["defaults"] or stripped != (defaults.get(key) or "").strip()
        ):
            current[key] = ""
    for key in spec["defaults"]:
        if not (current.get(key) or "").strip() and (defaults.get(key) or "").strip():
            current[key] = defaults[key]
    return current


def all_product_defaults(brand_kit: dict, current: dict | None = None) -> dict:
    """[브랜드 킷 기본값 채우기] — every default, again only into empty keys."""
    current = dict(current or {})
    for key, value in (brand_kit.get("product_defaults") or {}).items():
        if not (current.get(key) or "").strip() and (value or "").strip():
            current[key] = value
    return current
