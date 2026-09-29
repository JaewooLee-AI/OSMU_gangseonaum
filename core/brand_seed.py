"""사회적협동조합 강서나눔돌봄센터 / 우렁각시 홈서비스(가사관리) Brand Kit.

Everything here is lifted from the organization's own material rather than
invented, so the generated drafts cite facts it can actually stand behind:

- https://nanum1584.com/3 (가사관리 페이지 — 이용대상, 제공·미제공 서비스,
  관리사 교육·신원보증·배상보험, 우렁각시 홈서비스 게시판)
- 같은 페이지의 공지 이미지: 「26년 가사서비스 요금표」(2026년 기준),
  「서울형 가사서비스」 안내 포스터, 가사관리사 모집 안내
- https://nanum1584.com/ (기관소개 — 설립 배경, 미션, 2026년 8월 기준 종사자 현황)
- company/주간보호_v2.pdf, company/주간보호센터.pdf (강서나눔통합돌봄센터 ·
  케어누리 강서점의 방문요양·주간보호 안내 — 관련 기관 소개용으로만 씀)

The compliance guardrail is rebuilt for a *home-service* provider. The
original tenant's greenwashing rules (환경성 표시·광고) don't apply here; the
real exposure is 「표시·광고의 공정화에 관한 법률」 (결과 보장·최상급·요금 오표시),
the scope of the 「가사근로자의 고용개선 등에 관한 법률」 기관 인증 (기관 인증을
관리사 개인 자격처럼 쓰는 것), and — for posts that touch the center's
방문요양·주간보호 side — 노인장기요양보험법의 본인부담금 면제·할인 유인 금지와
의료 효과 주장. See ai_workers/guardrail.py.

`seed_if_empty()` runs once on first launch; after that the Brand Kit page is
the source of truth and this file is never re-applied, so admin edits are
never clobbered.
"""
from __future__ import annotations

from core import repo

# --- visual identity --------------------------------------------------------
# 강서나눔돌봄센터 로고(나눔 그린 + 주황 하트)와 가사관리 페이지 안내물에서 뽑은
# 팔레트. Flet 테마(flet_app/theme.py)가 이 값을 그대로 씁니다.
BRAND_COLORS = {
    "primary": "#00703C",      # 나눔 그린 — 로고 워드마크
    "primary_dark": "#004D29",
    "secondary": "#0C5430",    # 숲 그린 — 서울형 가사서비스 안내물 바탕
    "accent": "#E46C00",       # 하트 오렌지 — 로고 하트
    "mint": "#CCE4D8",         # 연녹 — 로고 보조색
    "bg": "#F7FAF6",           # 맑은 바탕
    "text": "#1F2A24",
    "text_muted": "#6B7A72",
}

BRAND_NAME = "사회적협동조합 강서나눔돌봄센터"
SUB_BRAND = "우렁각시 홈서비스"
HOMEPAGE = "https://nanum1584.com/"
NAVER_BLOG_ID = "nanum1584"
INSTAGRAM_HANDLE = "nanum1584"
INDUSTRY = "서울 강서·양천 지역 정부인증 가사서비스(청소·세탁·정리수납) 제공기관 (고용노동부 인증 사회적기업 · 사회적협동조합)"

PERSONA = (
    "강서나눔돌봄센터에서 가사서비스 상담과 가사관리사 배정을 맡고 있는 담당자의 목소리로 이야기합니다. "
    "매일 고객의 집 사정을 듣고 그 집에 맞는 관리사님과 일정을 맞추는 사람이라, "
    "'무엇을 해 드리고 무엇은 어려운지'를 정확하게 말합니다. "
    "돌봄 종사자들이 직접 세운 협동조합답게, 가사관리사를 전문 직업인으로 존중하는 말투를 지킵니다. "
    "'일하는 사람이 행복해야 돌봄 받는 사람도 행복하다'는 기관의 믿음을 설교하지 않고, "
    "교육·신원 확인·배상보험 같은 구체적인 장치로 보여 줍니다. "
    "바쁜 맞벌이 부부, 육아에 지친 부모, 혼자 사는 어르신의 하루를 먼저 떠올리는 다정하고 실무적인 화자입니다."
)

TONE_AND_MANNER = """- 존댓말을 씁니다. '~합니다'와 '~해요'를 자연스럽게 섞습니다.
- 한 문장은 40자 안팎에서 끊고, 한 문단은 2~3문장까지만 씁니다. 같은 뜻을 두 번 말하지 않습니다.
- 첫 문단은 기관 자랑이 아니라 독자의 생활 장면(퇴근 후 쌓인 설거지, 주말마다 밀리는 빨래 등)으로 엽니다.
- 일하는 사람은 항상 '가사관리사' 또는 '관리사님'으로 부릅니다. '파출부·가정부·아줌마·이모님'으로 부르지 않습니다. '가사도우미'는 검색어로만, '흔히 가사도우미라고 부르는'처럼 한 글에 한두 번 씁니다.
- 제공하는 서비스와 제공하지 않는 서비스를 정확히 구분합니다. 손걸레질, 아이·어르신 돌봄, 베란다 밖 유리창처럼 제공하지 않는 일을 해 드린다고 쓰지 않습니다.
- 요금·바우처·인원 같은 숫자는 확인된 것만, 기준 연도와 함께 씁니다. 바우처는 지원 조건(대상·금액 한도)을 빼고 말하지 않습니다.
- '완벽', '100%', '무조건', '책임지고' 같은 결과 보장 표현을 쓰지 않습니다. 대신 교육·신원 확인·보험·해피콜 같은 장치를 사실대로 설명합니다.
- 고객의 실명, 아파트 동·호수, 얼굴이 드러나는 내용은 쓰지 않습니다. 후기는 '강서구 맞벌이 가정'처럼 익명으로만 씁니다.
- 이모지는 한 문단에 최대 1개, 느낌표는 꼭 필요한 곳에만 씁니다.
- 매 글 끝에 상담 전화(02-2065-1584, 내선 3번)나 온라인 신청으로 이어지는 부드러운 한 문장을 남깁니다."""

CORE_FACTS = [
    "사회적협동조합 강서나눔돌봄센터는 낮은 임금과 불안정한 근무환경을 고민하던 돌봄 종사자들이 뜻을 모아 설립한, 조합원이 주인인 사회적협동조합이며 고용노동부 인증 사회적기업입니다.",
    "미션은 '일하는 사람이 행복해야, 돌봄 받는 사람도 행복합니다'이며, 1996년부터 쌓아 온 돌봄 경험에 지속적인 교육을 더해 서비스를 제공합니다.",
    "2026년 8월 기준 사회복지사 14명, 요양보호사 41명, 가사관리사 21명, 활동지원사 324명 등 350명이 넘는 돌봄 종사자가 일하고 있습니다.",
    "가사서비스는 '정부인증 가사서비스 제공기관'(고용노동부 가사서비스 인증기관)으로서 제공하며, 서비스 이름은 '우렁각시 홈서비스'입니다. 이 인증은 기관 단위 인증입니다.",
    "가사관리사는 심층 면접과 신원 확인을 거쳐 채용하고, NCS 표준 기반의 기본교육·보수교육(20~60시간)을 표준 커리큘럼·교재·매뉴얼로 진행합니다.",
    "가사관리사는 정기적으로 건강검진을 받고, 기관은 최대 1억 원 한도의 배상책임보험에 가입되어 있습니다.",
    "사전상담으로 고객 요구를 파악해 맞춤형으로 서비스하고, 정기 고객만족도 조사·모니터링과 고충에 응대하는 해피콜 제도를 운영합니다.",
    "주요 이용대상은 맞벌이 가정, 육아와 가사로 지친 전업주부, 1인 가구, 편찮거나 홀로 계신 어르신 가구이며, 서울 강서구·양천구에서 서비스합니다.",
    "기본 서비스는 환기, 설거지, 바닥 먼지 청소, 주방·욕실·현관 청소와 정리, 세탁(색상·옷감별 분류, 세탁기 최대 2회, 널기, 개기), 쓰레기 배출과 창문·조명·밸브·현관문 마무리 점검이며, 집에 준비된 청소용품·도구를 사용합니다.",
    "정기계약 고객에게는 가스후드 외면, 전자레인지, 베란다 청소, 간단한 다림질(2장 이내), 이불장·옷장 정리, 냉장고·주방 수납장 간단 정리를 추가로 제공합니다.",
    "제공하지 않는 서비스: 손 걸레질(막대걸레·밀대 사용), 분해가 필요한 가전 청소, 베란다 밖 유리창(1층 포함)·수족관·천장 청소, 장·서랍장 정리, 손빨래, 분류되지 않은 재활용품 배출, 노약자·자녀 돌봄, 반려동물 이·미용, 안전이 보장되지 않거나 전문자격이 필요한 업무.",
    "2026년 가사서비스 요금(평수 무관)은 3시간 정기 75,000원·일회성 85,000원, 3시간 30분 정기 87,500원·일회성 97,500원, 4시간 정기 100,000원·일회성 110,000원입니다. 추가요금은 복층 1회 10,000원, 공휴일 1회 20,000원, 가사서비스 1시간 25,000원입니다.",
    "2026년 특화서비스 요금은 정리수납 1인 기본 6시간 180,000원(주말 200,000원, 추가 1시간 30,000원), 음식조리 1시간당 30,000원입니다.",
    "서울형 가사서비스는 서울 거주 중위소득 180% 이하 임산부·맞벌이·다자녀 가정이 '탄생육아 몽땅정보통'에서 신청하며, 바우처 70만 원 한도에서 고용노동부 인증 가사서비스 업체를 이용하는 지원사업입니다. 센터의 서울형 정기고객 요금은 3시간 10회 700,000원입니다.",
    "당일 노쇼는 1회 차감되고, 3회 이상 일정 변경은 불가하며 부득이한 변경 시 1회 서비스 비용이 차감됩니다. 시간 내 서비스 내용은 협의할 수 있습니다.",
    "가사서비스 문의는 02-2065-1584(내선 3번), 온라인 신청은 nanum1584.housekeeping.co.kr, 주소는 서울 강서구 우장산로 2길 6, 1층입니다. 가사관리사는 경험이 없어도 지원할 수 있고 교육을 받은 뒤 근무를 시작합니다.",
    "센터는 가사관리 외에 방문요양·장애인 활동지원·병원동행·긴급돌봄을 제공하며, 강서나눔통합돌봄센터(케어누리 강서점, 강서구 수명로2길 96 신관 2층, 02-6958-9084)에서 주간보호(월~토 08:30~18:00)와 방문요양을 운영합니다.",
]

TERMINOLOGY = {
    "강서나눔돌봄센터": "정식 명칭 '사회적협동조합 강서나눔돌봄센터'. '강서 나눔 돌봄센터'처럼 띄어 쓰지 않습니다.",
    "우렁각시 홈서비스": "강서나눔돌봄센터 가사관리(가사서비스)의 서비스 이름. '우렁각시 홈서비스'로 띄어 씁니다.",
    "가사관리사": "센터에 소속되어 가사서비스를 제공하는 전문 종사자. 사람을 부를 때는 항상 이 말(또는 '관리사님')을 씁니다. 개인이 국가자격을 가진 것처럼 쓰지 않습니다.",
    "가사서비스": "청소·세탁·정리 등 집안일을 지원하는 서비스. 센터 메뉴명은 '가사관리'.",
    "정부인증 가사서비스 제공기관": "「가사근로자의 고용개선 등에 관한 법률」에 따라 고용노동부가 인증한 기관. 기관 단위 인증이므로 '정부인증 가사관리사', '국가공인 관리사'처럼 개인에게 붙이지 않습니다.",
    "서울형 가사서비스": "서울시 가사서비스 바우처 지원사업. 대상(서울 거주 중위소득 180% 이하 임산부·맞벌이·다자녀 가정)과 한도(70만 원)를 함께 씁니다. '무료'라고 쓰지 않습니다.",
    "탄생육아 몽땅정보통": "서울형 가사서비스를 신청하는 서울시 온라인 창구.",
    "정기계약": "정해진 주기로 이용하는 계약. 일회성보다 요금이 낮고 추가 서비스 항목이 붙습니다.",
    "일회성": "한 번만 이용하는 가사서비스. 정기와 요금이 다릅니다.",
    "정리수납": "옷장·주방 등 수납 공간을 정리하는 특화서비스. 1인 기본 6시간.",
    "음식조리": "1시간 단위로 이용하는 특화서비스.",
    "NCS": "국가직무능력표준. 가사관리사 교육의 기준. 'NCS 자격증'이 아니라 'NCS 표준 기반 교육'으로 씁니다.",
    "해피콜": "서비스 후 고객에게 전화로 만족도와 불편 사항을 확인하는 센터의 제도.",
    "배상책임보험": "서비스 중 물건 파손 등에 대비한 보험. 한도는 최대 1억 원이며, '전액 보상'처럼 쓰지 않습니다.",
    "사회적협동조합": "조합원(돌봄 종사자)이 주인인 비영리 법인 형태. 강서나눔돌봄센터의 법인 형태입니다.",
}

SEO_KEYWORDS = [
    "가사서비스",
    "가사도우미",
    "강서구 가사도우미",
    "양천구 가사도우미",
    "서울형 가사서비스",
    "가사관리사",
    "정부인증 가사서비스",
    "가사서비스 요금",
    "정리수납",
    "맞벌이 가사",
    "가사돌봄",
]

# 표시·광고의 공정화에 관한 법률 + 가사근로자법 인증 범위 + (방문요양·주간보호 글용)
# 노인장기요양보험법·의료법 기준의 결정론적 치환 사전.
# 여기 등록된 표현은 LLM이 무엇을 쓰든 발행 전 100% 자동 치환됩니다.
#
# 치환어를 고를 때의 원칙: **원래 표현과 같은 품사·활용형**을 씁니다. 한국어는
# 조사가 뒤에 붙기 때문에, 관형형('~한/~는')을 명사구로 바꾸면 "국내 최초로"가
# "국내에서도 보기 드문로" 같은 비문이 됩니다. 그래서
#   - 관형어 → 관형어 ("완벽한" → "꼼꼼한")
#   - 명사 → 명사 ("파출부" → "가사관리사")
#   - 부사 → 부사 ("완벽하게" → "꼼꼼하게")
# 로 맞추고, 조사가 붙는 형태('~로')는 별도 항목으로 함께 등록합니다.
# (긴 항목이 먼저 매칭되도록 하는 처리는 ai_workers/guardrail.py에 있습니다.)
#
# '가사도우미'는 SEO 키워드이므로 치환 대상이 아닙니다 — 치환하면 그 키워드는
# 밀도를 영원히 채우지 못합니다. 사람을 부르는 말로 쓰지 않는 규칙은 톤앤매너가 맡습니다.
BLACKLIST_MAP = {
    # --- 결과 보장·절대적 표현 (표시광고법) ---
    "100% 만족 보장": "고객 만족도 관리",
    "만족 보장": "만족도 관리",
    "100% 만족": "높은 만족",
    "완벽 청소": "꼼꼼한 청소",
    "완벽하게": "꼼꼼하게",
    "완벽한": "꼼꼼한",
    "무조건": "최대한",
    "책임지고": "성심껏",
    "전액 보상": "배상책임보험 한도 내 배상",
    # --- 최상급·배타적 표현 ---
    "국내 최초로": "국내에서도 보기 드물게",
    "국내 최초": "국내에서도 보기 드문",
    "업계 최고의": "업계에서 손꼽히는",
    "업계 최고": "업계에서 손꼽히는",
    "최고의 가사관리사": "숙련된 가사관리사",
    "유일한": "흔치 않은",
    # --- 기관 인증을 개인 자격·정부 보증으로 확대 (가사근로자법 인증 범위) ---
    "국가공인 가사관리사": "NCS 표준 교육을 이수한 가사관리사",
    "국가자격증을 가진 가사관리사": "NCS 표준 교육을 이수한 가사관리사",
    "정부인증 가사관리사": "정부인증 기관의 가사관리사",
    "정부가 보증하는": "정부인증 기관이 제공하는",
    "NCS 자격증": "NCS 표준 교육",
    # --- 바우처를 '무료'로 오표시 ---
    "무료 가사서비스": "바우처 지원 가사서비스",
    "무료로 이용": "바우처로 이용",
    "공짜로": "바우처로",
    # --- 종사자 비하 호칭 (브랜드 원칙: 가사관리사를 전문 직업인으로 부름) ---
    # '가정부'·'식모'는 등록하지 않습니다 — 치환이 부분 문자열 기준이라
    # "맞벌이 가정부터", "음식모임"까지 깨뜨립니다. 이 둘은 톤앤매너가 막습니다.
    "파출부": "가사관리사",
    "이모님": "관리사님",
    "아줌마": "관리사님",
    # --- 방문요양·주간보호 글: 본인부담금 유인(노인장기요양보험법), 의료 효과(의료법) ---
    "본인부담금 면제": "본인부담금 안내",
    "본인부담금 할인": "본인부담금 안내",
    "본인부담금 없이": "본인부담금 기준에 따라",
    "치매를 예방하는": "인지 활동을 돕는",
    "치매 예방": "인지 자극 활동",
    "치매 치료": "인지 활동 지원",
}

FEW_SHOT_SAMPLES = [
    """퇴근하고 현관문을 열었는데, 아침에 담가 둔 설거지가 그대로 있을 때가 있죠.

주말에 몰아서 하자고 미뤄 둔 빨래도 한 바구니고요. 쉬어야 할 주말이 집안일로 사라집니다.

그래서 저희 센터에 전화 주시는 분들 중에는 맞벌이 가정이 많아요.

우렁각시 홈서비스는 환기부터 시작합니다. 설거지와 바닥 먼지 청소, 주방·욕실·현관 정리를 하고요. 빨래는 색상과 옷감별로 나눠 세탁기를 돌리고, 널고, 마른 빨래까지 개어 둡니다. 마지막엔 쓰레기를 내놓고 창문과 밸브, 현관문을 한 번 더 확인해요.

미리 말씀드리는 것도 있어요. 손걸레질 대신 막대걸레와 밀대를 쓰고, 아이나 어르신 돌봄은 가사서비스에 포함되지 않습니다. 해 드릴 수 있는 일과 어려운 일을 처음부터 정확히 알려 드려야 서로 편하니까요.

오시는 관리사님은 심층 면접과 신원 확인을 거쳐 채용됐고, NCS 표준 기반 교육을 받았습니다. 혹시 모를 파손에 대비해 최대 1억 원 한도의 배상책임보험에도 가입되어 있어요.

2026년 기준 요금은 3시간 정기 75,000원, 일회성 85,000원입니다. 평수와 상관없이 같은 요금이에요.

서울 거주 중위소득 180% 이하 맞벌이 가정이라면 서울형 가사서비스 바우처(70만 원 한도)도 쓰실 수 있습니다.

주말을 돌려받고 싶으시다면, 02-2065-1584(내선 3번)로 편하게 상담부터 받아 보세요."""
]


def seed_if_empty() -> bool:
    """Populates the Brand Kit on first launch only. Returns True if seeded."""
    existing = repo.get_brand_kit()
    if existing.get("brand_name") or existing.get("persona"):
        return False

    repo.save_brand_kit(
        brand_name=BRAND_NAME,
        sub_brand=SUB_BRAND,
        industry=INDUSTRY,
        homepage=HOMEPAGE,
        naver_blog_id=NAVER_BLOG_ID,
        instagram_handle=INSTAGRAM_HANDLE,
        persona=PERSONA,
        tone_and_manner=TONE_AND_MANNER,
        core_facts=CORE_FACTS,
        terminology=TERMINOLOGY,
        seo_keywords=SEO_KEYWORDS,
        blacklist_map=BLACKLIST_MAP,
        few_shot_samples=FEW_SHOT_SAMPLES,
        guardrail_enabled=True,
        vision_enabled=True,
        vision_quality="economy",
    )
    return True


# One-time corrections to text an earlier version of this file seeded into
# existing Brand Kits. seed_if_empty() never touches a kit that already
# exists, so a fix to a seeded default would otherwise reach new installs
# only. Each (old, new) pair is applied once, and only where `old` is still
# present verbatim — i.e. the admin never edited that line — so admin edits
# are still never clobbered. Empty for a freshly set-up company.
SEED_FIXES: list = []
_SEED_FIXES_STATE_KEY = "brand_seed_fixes_applied"

# Same idea for the banned-term dictionary: entries added to BLACKLIST_MAP
# after a kit was seeded. Each key is added once, and only if the admin's
# dictionary doesn't already have it — an existing entry (with whatever
# replacement the admin chose) always wins. Empty for a new company.
SEED_BLACKLIST_ADDITIONS: dict = {}


def apply_seed_fixes() -> int:
    """Applies SEED_FIXES to the saved tone guide and SEED_BLACKLIST_ADDITIONS
    to the saved dictionary. Returns how many changes were made."""
    done = set((repo.get_app_state(_SEED_FIXES_STATE_KEY) or {}).get("done") or [])
    tone = repo.get_brand_kit().get("tone_and_manner") or ""
    applied = 0
    for old, new in SEED_FIXES:
        if old in done:
            continue
        if old in tone:
            tone = tone.replace(old, new)
            applied += 1
        done.add(old)
    if applied:
        repo.save_brand_kit(tone_and_manner=tone)

    blacklist = dict(repo.get_brand_kit().get("blacklist_map") or {})
    added = 0
    for term, replacement in SEED_BLACKLIST_ADDITIONS.items():
        marker = f"blacklist:{term}"
        if marker in done:
            continue
        if term not in blacklist:
            blacklist[term] = replacement
            added += 1
        done.add(marker)
    if added:
        repo.save_brand_kit(blacklist_map=blacklist)

    repo.set_app_state(_SEED_FIXES_STATE_KEY, {"done": sorted(done)})
    return applied + added
