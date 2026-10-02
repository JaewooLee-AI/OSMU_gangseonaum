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
# SNS 강화의 목적은 신규 사업(주간보호·방문요양)입니다 — 2026-10-03 담당자 확인. 그래서 기본 화자·
# 브랜드는 강서나눔통합돌봄센터이고, 가사서비스(우렁각시 홈서비스)는 가사 글 유형에서만 쓰는
# 보조 화자(HOUSE_VOICE)입니다. 가사서비스는 기존 고객 기반으로 운영되어 SNS 의존도가 낮습니다.
SUB_BRAND = "강서나눔통합돌봄센터"
HOMEPAGE = "https://nanum1584.com/"
NAVER_BLOG_ID = "nanum1584"
INSTAGRAM_HANDLE = "nanum1584"
INDUSTRY = (
    "서울 강서구 어르신 주간보호·방문요양(노인장기요양) 기관 강서나눔통합돌봄센터(케어누리 강서점)를 운영하는 "
    "돌봄기관. 같은 법인이 강서·양천 지역 정부인증 가사서비스(우렁각시 홈서비스)도 제공 "
    "(고용노동부 인증 사회적기업 · 사회적협동조합)"
)

HOUSE_PERSONA = (
    "강서나눔돌봄센터에서 가사서비스 상담과 가사관리사 배정을 맡고 있는 담당자의 목소리로 이야기합니다. "
    "매일 고객의 집 사정을 듣고 그 집에 맞는 관리사님과 일정을 맞추는 사람이라, "
    "'무엇을 해 드리고 무엇은 어려운지'를 정확하게 말합니다. "
    "돌봄 종사자들이 직접 세운 협동조합답게, 가사관리사를 전문 직업인으로 존중하는 말투를 지킵니다. "
    "'일하는 사람이 행복해야 돌봄 받는 사람도 행복하다'는 기관의 믿음을 설교하지 않고, "
    "교육·신원 확인·배상보험 같은 구체적인 장치로 보여 줍니다. "
    "바쁜 맞벌이 부부, 육아에 지친 부모, 혼자 사는 어르신의 하루를 먼저 떠올리는 다정하고 실무적인 화자입니다."
)

HOUSE_TONE = """- 존댓말을 씁니다. '~합니다'와 '~해요'를 자연스럽게 섞습니다.
- 한 문장은 40자 안팎에서 끊고, 한 문단은 2~3문장까지만 씁니다. 같은 뜻을 두 번 말하지 않습니다.
- 첫 문단은 기관 자랑이 아니라 독자의 생활 장면(퇴근 후 쌓인 설거지, 주말마다 밀리는 빨래 등)으로 엽니다.
- 일하는 사람은 항상 '가사관리사' 또는 '관리사님'으로 부릅니다. '파출부·가정부·아줌마·이모님'으로 부르지 않습니다. '가사도우미'는 검색어로만, '흔히 가사도우미라고 부르는'처럼 한 글에 한두 번 씁니다.
- 제공하는 서비스와 제공하지 않는 서비스를 정확히 구분합니다. 손걸레질, 아이·어르신 돌봄, 베란다 밖 유리창처럼 제공하지 않는 일을 해 드린다고 쓰지 않습니다.
- 요금·바우처·인원 같은 숫자는 확인된 것만, 기준 연도와 함께 씁니다. 바우처는 지원 조건(대상·금액 한도)을 빼고 말하지 않습니다.
- '완벽', '100%', '무조건', '책임지고' 같은 결과 보장 표현을 쓰지 않습니다. 대신 교육·신원 확인·보험·해피콜 같은 장치를 사실대로 설명합니다.
- 고객의 실명, 아파트 동·호수, 얼굴이 드러나는 내용은 쓰지 않습니다. 후기는 '강서구 맞벌이 가정'처럼 익명으로만 씁니다.
- 이모지는 한 문단에 최대 1개, 느낌표는 꼭 필요한 곳에만 씁니다.
- 매 글 끝에 상담 전화(02-2065-1584, 내선 3번)나 온라인 신청으로 이어지는 부드러운 한 문장을 남깁니다."""

# --- 주간보호·방문요양 사업 분야 ------------------------------------------------
# 출처: company/주간보호센터.pdf(주간보호 전단), company/주간보호_v2.pdf(케어누리 강서점 리플릿).
# 운영 관계(같은 법인 운영)는 2026-10-03 담당자 확인. 전단에 없는 것 — 본인부담금·비용,
# 정원, 등급별 이용 가능 여부, 집 앞 송영 여부 — 은 넣지 않았습니다.
CARE_FACTS = [
    "센터는 가사관리 외에 방문요양·장애인 활동지원·병원동행·긴급돌봄을 제공하며, 같은 법인이 강서나눔통합돌봄센터(케어누리 강서점)를 운영해 주간보호와 방문요양을 제공합니다.",
    "강서나눔통합돌봄센터(케어누리 강서점) 주간보호는 월~토 08:30~18:00 운영하며, 이용 대상은 노인장기요양등급 판정을 받은 어르신입니다.",
    "주간보호 프로그램은 인지&신체 통합 프로그램, 실버노래교실, 그림책 프로그램, 재활운동 프로그램, 실버미술 프로그램이며, 재활운동 특화 주간보호센터입니다.",
    "주간보호에서는 위생관리(이미용서비스, 샤워지원 등), 차량 송영, 균형 잡힌 식사와 간식을 제공합니다.",
    "주간보호 송영 지역은 등촌동, 가양동, 마곡동, 발산동, 우장산동, 공항동, 방화동, 화곡동 등 강서구 일대입니다.",
    "방문요양은 국가 자격증을 가진 요양보호사가 장기요양 인정을 받은 어르신 댁을 방문해 신체활동 지원(세면·구강관리, 식사 준비 및 도움, 몸단장), 가사 및 일상생활 지원(취사·청소·세탁, 장보기·외출 동행), 정서 지원(말벗, 심리 안정), 인지생활 지원(인지자극 프로그램, 기능회복훈련)을 제공하는 재가 장기요양 서비스입니다.",
    "방문요양 대상은 만 65세 이상으로 거동이 불편해 일상생활을 혼자 하기 어려운 어르신, 그리고 65세 미만이라도 치매·뇌혈관질환(뇌졸중 등)·파킨슨병 등 노인성 질병이 있는 분입니다.",
    "강서나눔통합돌봄센터 위치는 서울 강서구 수명로2길 96 은강회복지재단 신관 2층(수명산8단지 옆)이며, 5호선 마곡역 5번 출구에서 1.1km, 우장산역 4번 출구에서 1.2km입니다. 주간보호·방문요양 상담은 02-6958-9084입니다.",
    "케어누리는 어르신과 돌봄 가족뿐 아니라 요양보호사까지 모두가 존중받는 '존엄케어'를 실천합니다 — 어르신을 고유한 삶의 경험을 지닌 주체적인 인격체로 존중하고, 요양보호사를 전문 직업인으로 존중합니다.",
]

# 기본 화자 — 주간보호·방문요양. 브랜드 킷 화면의 '브랜드 페르소나·톤앤매너'가 이 값입니다.
PERSONA = (
    "강서나눔통합돌봄센터(케어누리 강서점)에서 주간보호·방문요양 상담을 맡고 있는 담당자의 목소리로 이야기합니다. "
    "부모님 돌봄을 고민하는 자녀와 보호자의 사정을 먼저 듣고, 어르신을 고유한 삶의 경험을 지닌 분으로 존중하는 "
    "'존엄케어'의 태도를 지킵니다. 돌봄 종사자들이 세운 사회적협동조합이 운영하는 기관답게 요양보호사를 전문 "
    "직업인으로 존중합니다. 무엇을 해 드릴 수 있는지를 정확히 말하되, 건강이 좋아진다거나 등급을 받게 해 드린다는 "
    "약속은 하지 않는 차분하고 다정한 화자입니다."
)
CARE_PERSONA = PERSONA  # 이전 이름 호환

TONE_AND_MANNER = """- 존댓말을 씁니다. '~합니다'와 '~해요'를 자연스럽게 섞습니다.
- 한 문장은 40자 안팎에서 끊고, 한 문단은 2~3문장까지만 씁니다. 같은 뜻을 두 번 말하지 않습니다.
- 첫 문단은 기관 자랑이 아니라 보호자의 생활 장면(출근길 부모님 걱정, 홀로 계신 부모님의 낮 시간 등)으로 엽니다.
- 이용하시는 분은 '어르신', 돌봄 인력은 '요양보호사' 또는 '선생님'으로 부릅니다. '노치원' 같은 속칭은 쓰지 않습니다. '데이케어센터'는 '주간보호센터(데이케어센터)'처럼 함께 쓸 수 있습니다.
- 프로그램이 근력·인지 기능을 회복시킨다·지켜 준다·예방한다고 단정하지 않습니다. '참여하실 수 있습니다', '함께합니다'처럼 활동 자체를 설명합니다.
- 비용·본인부담금·등급별 이용 조건처럼 자료에 없는 내용은 쓰지 말고 '상담으로 안내해 드립니다'로 넘깁니다. 장기요양등급을 받게 해 준다고 쓰지 않습니다.
- 하루 일과는 핵심 팩트에 있는 것(송영, 프로그램, 식사와 간식, 위생관리)만 씁니다. 집 앞·문 앞 송영, 도착 후 체온·건강 체크, 식사 형태(죽·다진 음식 등), 차 대접처럼 자료에 없는 절차를 장면 묘사로 지어내지 않습니다.
- 어르신의 실명, 얼굴이 드러나는 사진·내용은 쓰지 않습니다. 현장 이야기는 '화곡동에 사시는 80대 어르신'처럼 익명으로만 씁니다.
- 이모지는 한 문단에 최대 1개, 느낌표는 꼭 필요한 곳에만 씁니다.
- 매 글 끝에 상담 전화(02-6958-9084, 강서나눔통합돌봄센터)로 이어지는 부드러운 한 문장을 남깁니다."""

# 주간보호 글(글 유형 'care')의 🧹 서비스·이용 정보 기본값. 전부 CARE_FACTS에 있는 내용입니다.
CARE_PRODUCT_DEFAULTS = {
    "moq": "노인장기요양등급 판정을 받은 어르신 · 주간보호 월~토 08:30~18:00",
    "size": "인지&신체 통합·실버노래교실·그림책·재활운동·실버미술 프로그램, 위생관리(이미용·샤워 지원), 차량 송영, 식사와 간식",
    "options": "송영 지역: 등촌동·가양동·마곡동·발산동·우장산동·공항동·방화동·화곡동 등 강서구 일대",
    "order": "상담 02-6958-9084 (강서나눔통합돌봄센터, 강서구 수명로2길 96 신관 2층)",
}

# 핵심 팩트는 하나의 목록이지만 '법인 공통 → 돌봄센터(주력) → 가사서비스' 순서로 둡니다. 모든 글과
# 검수에 전체가 들어가므로 기능상 차이는 없고, 브랜드 킷 화면에서 사람이 읽고 고치기 쉽게 하려는 것입니다.
COMMON_FACTS = [
    "사회적협동조합 강서나눔돌봄센터는 낮은 임금과 불안정한 근무환경을 고민하던 돌봄 종사자들이 뜻을 모아 설립한, 조합원이 주인인 사회적협동조합이며 고용노동부 인증 사회적기업입니다.",
    "미션은 '일하는 사람이 행복해야, 돌봄 받는 사람도 행복합니다'이며, 1996년부터 쌓아 온 돌봄 경험에 지속적인 교육을 더해 서비스를 제공합니다.",
    "2026년 8월 기준 사회복지사 14명, 요양보호사 41명, 가사관리사 21명, 활동지원사 324명 등 350명이 넘는 돌봄 종사자가 일하고 있습니다.",
    CARE_FACTS[0],
]

HOUSE_FACTS = [
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
]

# 장기요양 제도 정보 — 보호자가 가장 많이 찾는 정보(장기요양등급신청 월 10,640회, 장기요양등급기준
# 8,000회)라 정보 글의 근거로 둡니다. 회사 사실이 아니라 공개된 제도이므로 문장마다 출처를 붙였고,
# 2026-10-03 원문 확인: 국민건강보험공단 장기요양 안내(nhis.or.kr/static/html/wbda/c/wbdac02~05.html),
# 국가법령정보센터 노인장기요양보험법 제16조·제40조, 시행령 제8조(2026.5.12 개정).
# 공단 안내의 '재가급여 월 한도액' 표는 2020년 기준이라 넣지 않았습니다. 법·고시가 바뀌면 고치세요.
# '[제도 정보'로 시작하는 팩트는 가사서비스 글에는 넣지 않습니다 (content_writer._brand_kit_for).
INFO_FACT_PREFIX = "[제도 정보"
INFO_FACTS = [
    "[제도 정보 · 출처: 국민건강보험공단] 장기요양인정은 장기요양보험 가입자와 피부양자, 의료급여수급권자 가운데 65세 이상 노인, 또는 65세 미만이라도 치매·뇌혈관질환 등 노인성 질병이 있는 사람이 신청할 수 있으며, 본인 또는 가족·친족 등 대리인이 신청할 수 있습니다.",
    "[제도 정보 · 출처: 국민건강보험공단] 신청은 국민건강보험공단 지사(장기요양운영센터) 방문, 우편, 팩스로 할 수 있고, 인터넷 신청은 65세 이상(또는 65세 미만의 갱신 신청)인 경우 노인장기요양보험 홈페이지(www.longtermcare.or.kr)에서 할 수 있습니다. 장기요양인정신청서와 의사소견서를 내며, 65세 이상은 의사소견서를 등급판정위원회 심의 전까지 내도 됩니다.",
    "[제도 정보 · 출처: 국민건강보험공단] 신청하면 공단 직원이 신청인의 거주지를 방문해 90개 항목의 장기요양인정조사표로 심신 상태를 조사하고, 그 결과와 의사소견서를 바탕으로 장기요양등급판정위원회가 등급을 정합니다.",
    "[제도 정보 · 출처: 노인장기요양보험법 제16조] 등급판정은 신청서를 낸 날부터 30일 이내에 완료하는 것이 원칙이며, 정밀조사가 필요한 경우 등 부득이한 사유가 있으면 30일 이내의 범위에서 연장될 수 있습니다.",
    "[제도 정보 · 출처: 국민건강보험공단 등급판정 기준] 장기요양인정점수 기준은 1등급 95점 이상, 2등급 75점 이상 95점 미만, 3등급 60점 이상 75점 미만, 4등급 51점 이상 60점 미만, 5등급 45점 이상 51점 미만(치매 환자), 인지지원등급 45점 미만(치매 환자)입니다.",
    "[제도 정보 · 출처: 국민건강보험공단] 1~5등급과 인지지원등급 인정을 받은 분은 장기요양인정서와 표준장기요양이용계획서가 도달한 날부터 장기요양기관과 계약해 급여를 이용할 수 있으며, 재가급여에는 방문요양·방문목욕·방문간호·주야간보호·단기보호 등이 있습니다.",
    "[제도 정보 · 출처: 국민건강보험공단, 노인장기요양보험법 제40조] 재가급여(방문요양·주야간보호 등) 이용자는 장기요양 급여비용의 15%를 본인이 부담합니다. 국민기초생활보장법에 따른 의료급여 수급자(의료급여법 제3조제1항제1호)는 본인부담금을 내지 않고, 그 밖의 의료급여 수급권자와 소득·재산이 일정 기준 이하인 분은 본인부담금이 감경되며, 급여 범위에 포함되지 않는 비용은 본인이 전부 부담합니다.",
    "[제도 정보 · 출처: 노인장기요양보험법 시행령 제8조] 장기요양인정 유효기간은 2년이며, 갱신하면 1등급 5년, 2~4등급 4년, 5등급과 인지지원등급 2년입니다.",
]
INFO_TONE_RULE = "제도 정보(장기요양등급·신청 절차·본인부담률·유효기간)는 '[제도 정보]' 팩트 그대로 쓰고 출처(국민건강보험공단 등)를 밝힙니다. 등급은 공단 등급판정위원회가 정한다는 점을 분명히 하고, 센터가 대신 신청해 준다·등급을 받게 해 준다고 쓰지 않습니다. 감경·본인부담 없음은 법정 기준 그대로만 설명하고 센터 이용 혜택처럼 쓰지 않습니다."

CORE_FACTS = [*COMMON_FACTS, *CARE_FACTS[1:], *INFO_FACTS, *HOUSE_FACTS]
TONE_AND_MANNER = TONE_AND_MANNER + "\n- " + INFO_TONE_RULE

CARE_TERMINOLOGY = {
    "강서나눔통합돌봄센터": "같은 법인이 운영하는 주간보호·방문요양 기관. 케어누리 강서점. '강서나눔돌봄센터'(가사서비스 문의처)와 전화번호가 다릅니다(02-6958-9084).",
    "케어누리 강서점": "강서나눔통합돌봄센터가 함께 쓰는 이름. '케어누리 강서점'으로 띄어 씁니다.",
    "주간보호": "장기요양등급을 받은 어르신이 낮 시간 센터에서 프로그램·식사·위생관리를 받는 서비스. '노치원' 같은 속칭은 쓰지 않습니다.",
    "방문요양": "요양보호사가 어르신 댁을 방문하는 재가 장기요양 서비스. 가사서비스(우렁각시 홈서비스)와 다른 서비스입니다.",
    "요양보호사": "방문요양·주간보호에서 일하는 국가 자격 돌봄 인력. 가사관리사와 다른 직종입니다.",
    "노인장기요양등급": "국민건강보험공단의 장기요양 인정 판정. 센터가 등급을 받게 해 주는 것처럼 쓰지 않습니다.",
    "송영": "주간보호 이용 어르신을 차량으로 모셔 오고 모셔다 드리는 것.",
    "데이케어센터": "주간보호센터를 부르는 다른 이름. 보호자가 이 말로 많이 검색하므로(강서구 데이케어센터 월 100회) '주간보호센터(데이케어센터)'처럼 함께 써도 됩니다.",
    "존엄케어": "케어누리의 돌봄 이념. 어르신·가족·요양보호사 모두가 존중받는 돌봄.",
    "은강회복지재단": "강서나눔통합돌봄센터가 있는 건물(신관 2층)의 이름. '은강'으로 씁니다.",
}

COMMON_TERMINOLOGY = {
    "강서나눔돌봄센터": "정식 명칭 '사회적협동조합 강서나눔돌봄센터'. '강서 나눔 돌봄센터'처럼 띄어 쓰지 않습니다.",
    "사회적협동조합": "조합원(돌봄 종사자)이 주인인 비영리 법인 형태. 강서나눔돌봄센터의 법인 형태입니다.",
}

HOUSE_TERMINOLOGY = {
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
}

# 법인 공통 → 돌봄센터(주력) → 가사서비스 순서 (핵심 팩트와 같은 이유).
TERMINOLOGY = {**COMMON_TERMINOLOGY, **CARE_TERMINOLOGY, **HOUSE_TERMINOLOGY}

SEO_KEYWORDS = [
    # 돌봄센터(주력) — 2026-10-03 검색광고 실측: 강서구 방문요양 월 290, 강서구 주간보호센터 190,
    # 강서구 데이케어센터 100, 화곡동 주간보호센터 25.
    "강서구 방문요양",
    "강서구 주간보호센터",
    "강서구 데이케어센터",
    "화곡동 주간보호센터",
    # 가사서비스
    "가사서비스",
    "가사도우미",
    "강서구 가사도우미",
    "양천구 가사도우미",
    "서울형 가사서비스",
    "가사관리사",
    "정부인증 가사서비스",
    "정리수납",
    "가사돌봄",
    # (가사서비스 요금·맞벌이 가사는 월 10회 = 측정 하한이라 뺐습니다.)
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
    # 자료에는 '70만 원 한도'만 있고 기간(연간 등)은 없습니다. 실측 첫 생성에서 모델이
    # '연간 70만 원'을 붙였고, 블로그 본문을 참고하는 SNS 4채널에 그대로 번졌습니다.
    "연간 70만 원": "70만 원",
    "연 70만 원": "70만 원",
    # 송영은 '차량 송영'까지만 확인됐습니다 — 집 앞(문 앞) 여부는 자료에 없습니다.
    "댁 앞까지": "댁까지",
    "집 앞까지": "댁까지",
    # 센터 건물 이름 오기 — 실측 생성에서 '은광회복지재단'으로 나왔습니다(맞춤법 교정은 고유명사라 못 잡음).
    "은광회복지재단": "은강회복지재단",
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

# 본문에는 계속 쓰되 글의 SEO 타깃·제목 키워드로는 쓰지 않을 말.
# '가사관리사'는 톤앤매너가 사람을 부를 때 반드시 쓰라고 정한 호칭이라 거의 모든 글에서
# 가장 많이 나오고, 그래서 타깃 선정(초안에 많이 나온 키워드 우선)이 매번 이 말을 골라
# 제목에까지 밀어 넣었습니다. 그런데 이 말로 검색하는 사람은 대부분 자격·취업 정보를
# 찾는 구직자입니다. 관리사 모집 글을 쓸 때는 브랜드 킷에서 이 체크를 잠시 풀면 됩니다.
NON_TARGET_KEYWORDS = ["가사관리사"]

# 서비스 지역 — 핵심 팩트의 '서울 강서구·양천구'와 그 안의 동·생활권 이름입니다.
# 동네 키워드 후보('화곡동 가사도우미' 등)와 지역 해시태그의 재료로 쓰입니다.
# 검색량은 ⚙️ 설정 → 🔑 SEO 키워드 → [📍 동네 키워드 찾기]에서 실제로 잰 뒤 고릅니다.
HOUSE_SERVICE_AREAS = [
    "강서구", "양천구",
    "화곡동", "등촌동", "염창동", "가양동", "마곡", "발산", "우장산동", "공항동", "방화동",
    "목동", "신정동", "신월동",
]

# 🧹 서비스·이용 정보 시트의 기본값. 전부 위 CORE_FACTS에 이미 있는 내용이고, 확인되지 않은
# 항목(예: 신청 후 시작까지 걸리는 기간)은 비워 둡니다 — 이 값은 '반드시 본문에 넣을 사실'로
# 모델에 전달되므로, 여기 적는 순간 회사의 약속이 됩니다.
PRODUCT_DEFAULTS = {
    "price": "3시간 정기 75,000원 / 일회성 85,000원 (2026년 기준, 평수 무관)",
    "moq": "정기계약 또는 일회성 (3시간 · 3시간 30분 · 4시간)",
    "size": "환기, 설거지, 바닥 먼지 청소, 주방·욕실·현관 청소와 정리, 세탁(최대 2회)·널기·개기, 쓰레기 배출",
    "options": "정리수납 1인 기본 6시간 180,000원 / 음식조리 1시간 30,000원 (2026년 기준)",
    "custom": "서울형 가사서비스 바우처 — 서울 거주 중위소득 180% 이하 임산부·맞벌이·다자녀 가정, 70만 원 한도",
    "order": "02-2065-1584 (내선 3번) / 온라인 신청 nanum1584.housekeeping.co.kr",
}

# 뉴스 큐레이션에서 빼고 보여줄 기사 제목 단어. '가사도우미'로 뉴스를 찾으면 외국인
# 가사관리사 시범사업 기사가 섞여 들어오는데, 이 기관의 서비스와 무관하고 정책 논쟁이
# 큰 주제라 브랜드 글의 소재로 엮으면 위험합니다. 브랜드 킷 화면에서 고칠 수 있습니다.
NEWS_EXCLUDE_TERMS = ["외국인 가사관리사", "필리핀 가사관리사", "외국인 가사도우미", "필리핀 가사도우미"]

# 📅 주제 캘린더 — 대시보드가 이번 달 주제를 제안하고, 누르면 메모가 채워진 새 글이
# 만들어집니다. month 0은 언제든 쓸 수 있는 상시 주제입니다.
#
# 메모는 '무엇을 다룰지'만 적습니다. 회사 사실은 브랜드 킷에서 오고, 현장 이야기는
# 담당자가 [ ] 자리에 직접 채웁니다 — 비워 둔 채 생성하면 그 부분은 일반적인 설명으로
# 대신 쓰입니다. 제공하지 않는 서비스(손걸레질, 분해 가전 청소, 베란다 밖 유리창, 돌봄 등)를
# 끌어들이는 주제는 넣지 않았습니다.
TOPIC_CALENDAR = [
    {"month": 1, "post_type": "service", "title": "새해 맞이 집 정리, 정리수납 서비스로 시작하기",
     "memo": "새해에 옷장·주방 수납을 한 번에 정리하고 싶은 가정을 위한 정리수납 특화서비스 소개.\n현장 사례: [ ]"},
    {"month": 1, "post_type": "tip", "title": "설 명절 전 대청소 체크리스트",
     "memo": "설 명절 손님맞이 전에 주방·욕실·현관을 정리하는 순서. 정기·일회성 가사서비스로 맡길 수 있는 범위도 함께.\n현장에서 자주 받는 요청: [ ]"},
    {"month": 2, "post_type": "tip", "title": "명절 뒤 주방 정리, 이것부터",
     "memo": "명절 뒤 쌓인 설거지와 주방 정리 요령. 정기계약 고객에게 추가로 제공하는 냉장고·주방 수납장 간단 정리 안내.\n현장 사례: [ ]"},
    {"month": 3, "post_type": "service", "title": "이사철 정리수납, 새집에서 처음부터 제자리 찾기",
     "memo": "이사 뒤 짐 정리를 정리수납 특화서비스(1인 기본 6시간)로 맡기는 경우. 무엇을 해 주는지 구체적으로.\n현장 사례: [ ]"},
    {"month": 3, "post_type": "tip", "title": "봄맞이 대청소, 환기부터 바닥 먼지까지",
     "memo": "봄철 미세먼지가 쌓이기 쉬운 곳과 환기·바닥 먼지 청소 순서. 가사서비스가 매번 하는 환기부터 마무리 점검까지의 흐름.\n담당자 메모: [ ]"},
    {"month": 4, "post_type": "voucher", "title": "서울형 가사서비스, 우리 집도 받을 수 있을까",
     "memo": "서울형 가사서비스 바우처 대상 조건과 한도, 신청 창구(탄생육아 몽땅정보통), 센터에서 이용하는 방법.\n자주 받는 질문: [ ]"},
    {"month": 5, "post_type": "service", "title": "가정의 달, 부모님 댁에 가사서비스를",
     "memo": "홀로 계신 부모님 댁 집안일을 정기 가사서비스로 돕는 방법. 돌봄(신변 수발)은 가사서비스에 포함되지 않는다는 점도 정확히.\n현장 사례: [ ]"},
    {"month": 6, "post_type": "tip", "title": "장마 오기 전, 욕실·주방 습기 관리",
     "memo": "장마 전에 해 두면 좋은 욕실·주방 청소와 환기. 가사서비스로 맡길 수 있는 범위.\n담당자 메모: [ ]"},
    {"month": 7, "post_type": "tip", "title": "장마철 빨래, 냄새 없이 말리는 순서",
     "memo": "장마철 빨래 분류·세탁·널기 요령. 가사서비스의 세탁(색상·옷감별 분류, 세탁기 최대 2회, 널기, 개기) 안내.\n현장 사례: [ ]"},
    {"month": 8, "post_type": "service", "title": "휴가 다녀온 뒤 밀린 집안일, 일회성 가사서비스",
     "memo": "여름휴가 뒤 쌓인 빨래와 집안일을 일회성 가사서비스로 한 번에. 정기와 일회성의 차이도 함께.\n현장 사례: [ ]"},
    {"month": 8, "post_type": "service", "title": "개학 전 아이 방 정리수납",
     "memo": "개학 준비로 아이 방 옷장·책상 주변을 정리수납 특화서비스로 정리하는 경우. 아이 돌봄은 포함되지 않습니다.\n현장 사례: [ ]"},
    {"month": 9, "post_type": "tip", "title": "추석 손님맞이 전 집 정리",
     "memo": "추석 전에 현관·거실·주방을 정리하는 순서와, 명절 전 일정이 몰리니 미리 상담받으면 좋은 이유.\n담당자 메모: [ ]"},
    {"month": 10, "post_type": "service", "title": "환절기 옷장 정리, 정리수납으로 한 번에",
     "memo": "계절이 바뀔 때 옷장·이불장을 정리하는 정리수납 특화서비스. 정기계약 고객의 이불장·옷장 정리 추가 항목도.\n현장 사례: [ ]"},
    {"month": 11, "post_type": "tip", "title": "겨울 오기 전 주방·베란다 정리",
     "memo": "겨울 전 주방과 베란다(안쪽) 정리. 정기계약 고객에게 제공하는 베란다 청소 안내 — 베란다 밖 유리창은 제공하지 않습니다.\n담당자 메모: [ ]"},
    {"month": 12, "post_type": "tip", "title": "연말 대청소, 한 해 묵은 집안일 정리",
     "memo": "연말에 몰아서 하는 대청소를 일회성 가사서비스로 나눠 맡기는 방법.\n현장 사례: [ ]"},
    {"month": 12, "post_type": "service", "title": "새해부터 정기 가사서비스로 주말 되찾기",
     "memo": "새해 계획으로 정기 가사서비스를 시작하는 맞벌이 가정. 정기계약 요금과 추가 제공 항목.\n현장 사례: [ ]"},
    {"month": 0, "post_type": "service", "title": "우렁각시 홈서비스 요금 한눈에 보기",
     "memo": "2026년 가사서비스 요금표(정기·일회성, 시간별, 추가요금)와 특화서비스(정리수납·음식조리) 요금 정리."},
    {"month": 0, "post_type": "service", "title": "정기 vs 일회성, 우리 집엔 뭐가 맞을까",
     "memo": "정기계약과 일회성 가사서비스의 요금 차이와 정기계약에만 붙는 추가 항목 비교."},
    {"month": 0, "post_type": "service", "title": "가사서비스로 해 드리는 일, 어려운 일",
     "memo": "제공하는 서비스와 제공하지 않는 서비스를 질문·답변 형식으로 정확히 정리."},
    {"month": 0, "post_type": "service", "title": "믿고 맡길 수 있는 이유 — 교육·신원 확인·배상보험",
     "memo": "가사관리사 채용(심층 면접·신원 확인), NCS 표준 기반 교육, 건강검진, 최대 1억 원 배상책임보험, 해피콜 제도."},
    {"month": 0, "post_type": "voucher", "title": "서울형 가사서비스 신청부터 이용까지",
     "memo": "서울형 가사서비스 대상·한도·신청 창구와 센터의 서울형 정기고객 요금(3시간 10회)."},
    {"month": 0, "post_type": "review", "title": "맞벌이 가정의 정기 가사서비스 이용기",
     "memo": "[동네] 맞벌이 가정 정기 이용 사례. 요청한 일: [ ] / 해피콜에서 들은 말: [ ]\n※ 실명·동호수·얼굴은 쓰지 않습니다."},
    {"month": 0, "post_type": "review", "title": "1인 가구의 일회성 가사서비스 이용기",
     "memo": "[동네] 1인 가구 일회성 이용 사례. 요청한 일: [ ] / 고객 반응: [ ]\n※ 실명·동호수·얼굴은 쓰지 않습니다."},
    # 신규 사업(주간보호·방문요양)이 SNS 강화의 대상이라 달마다 돌봄 주제를 하나 이상 둡니다.
    {"month": 1, "post_type": "care", "title": "새해, 부모님 돌봄 계획 — 주간보호와 방문요양 차이",
     "memo": "새해를 맞아 부모님 돌봄을 계획하는 가족을 위한 주간보호·방문요양 비교. 각각 무엇을 해 드리는지, 대상이 누구인지.\n자주 받는 질문: [ ]"},
    {"month": 2, "post_type": "care", "title": "설 연휴에 본 부모님, 낮 시간 돌봄이 필요하다면",
     "memo": "명절에 부모님을 뵙고 낮 시간 돌봄을 고민하게 된 자녀를 위한 주간보호 안내 — 이용 대상, 운영 시간, 송영 지역.\n상담에서 자주 듣는 고민: [ ]"},
    {"month": 3, "post_type": "care_story", "title": "봄맞이 실버미술 시간 — 주간보호센터의 하루",
     "memo": "실버미술·그림책 프로그램 시간의 현장 이야기. 활동 내용만 쓰고 효과는 단정하지 않습니다.\n있었던 일: [ ]"},
    {"month": 4, "post_type": "care", "title": "재활운동 특화 주간보호, 어떤 프로그램을 하나요",
     "memo": "재활운동 특화 주간보호센터의 프로그램 소개(인지&신체 통합, 재활운동). 회복·예방 효과는 단정하지 않습니다.\n프로그램 현장 이야기: [ ]"},
    {"month": 6, "post_type": "care", "title": "방문요양, 요양보호사 선생님이 댁에서 해 드리는 일",
     "memo": "방문요양에서 요양보호사가 해 드리는 일(신체활동·가사 및 일상생활·정서·인지생활 지원)과 대상.\n자주 받는 질문: [ ]"},
    {"month": 8, "post_type": "care_story", "title": "실버노래교실이 열리는 오후",
     "memo": "실버노래교실 시간의 현장 이야기. 어르신 실명·얼굴 없이 익명으로.\n있었던 일: [ ]"},
    {"month": 10, "post_type": "care", "title": "강서구 주간보호센터(데이케어센터) 고르기 전에 확인할 것",
     "memo": "주간보호센터를 처음 알아보는 보호자를 위한 확인 목록 — 이용 대상(장기요양등급), 운영 시간, 송영 지역, 프로그램, 식사·위생관리, 상담. 다른 센터와 비교하거나 깎아내리지 않습니다.\n자주 받는 질문: [ ]"},
    {"month": 11, "post_type": "care", "title": "추워지기 전에, 차량 송영으로 다니는 주간보호",
     "memo": "날이 추워지면 외출이 어려운 어르신을 위한 차량 송영과 주간보호 하루 일과. 송영 지역 안내.\n현장 이야기: [ ]"},
    {"month": 5, "post_type": "care", "title": "가정의 달, 부모님 낮 시간 돌봄 — 주간보호 알아보기",
     "memo": "홀로 계신 부모님의 낮 시간이 걱정되는 자녀를 위한 주간보호 안내. 이용 대상(장기요양등급), 운영 시간, 송영.\n상담에서 자주 듣는 고민: [ ]"},
    {"month": 7, "post_type": "care", "title": "무더운 여름, 어르신 낮 시간을 함께 보내는 주간보호",
     "memo": "더운 낮에 집에 홀로 계신 어르신을 위한 주간보호의 하루 — 송영, 식사와 간식, 프로그램. 건강 효과를 단정하지 않습니다.\n현장 이야기: [ ]"},
    {"month": 9, "post_type": "care", "title": "명절에 살펴본 부모님, 방문요양과 주간보호 중 무엇이 맞을까",
     "memo": "명절에 부모님을 뵙고 돌봄을 고민하게 된 가족을 위한 방문요양·주간보호 비교. 각각 무엇을 해 드리는지, 대상이 누구인지.\n자주 받는 질문: [ ]"},
    {"month": 12, "post_type": "care", "title": "추운 겨울, 송영으로 오가는 주간보호",
     "memo": "추운 날 외출이 어려운 어르신을 위한 차량 송영과 주간보호 하루 일과. 송영 지역 안내.\n현장 이야기: [ ]"},
    # 보호자 정보 글 — [제도 정보] 팩트만 근거로 씁니다. 보호자가 '등급 신청 → 기관 찾기' 순으로 움직이므로
    # 상담 유입의 입구입니다 (장기요양등급신청 월 10,640회, 검색 1회당 경쟁 글 38개).
    {"month": 0, "post_type": "care_guide", "title": "장기요양등급 신청 방법, 처음부터 차근차근",
     "memo": "장기요양등급 신청 자격, 신청처와 방법, 제출 서류, 방문조사부터 판정까지의 순서와 기간. 등급은 공단이 정한다는 점을 분명히.\n보호자에게 자주 듣는 질문: [ ]"},
    {"month": 0, "post_type": "care_guide", "title": "장기요양등급 기준, 1등급부터 인지지원등급까지",
     "memo": "등급별 장기요양인정점수 기준과 심신 상태 설명. 점수는 공단 조사와 등급판정위원회가 정한다는 점.\n자주 받는 질문: [ ]"},
    {"month": 0, "post_type": "care_guide", "title": "등급을 받은 뒤, 주간보호·방문요양은 어떻게 이용하나요",
     "memo": "장기요양인정서를 받은 뒤 기관과 계약해 재가급여를 이용하는 순서. 주간보호(주야간보호)와 방문요양이 무엇인지, 센터 상담 안내.\n자주 받는 질문: [ ]"},
    {"month": 0, "post_type": "care_guide", "title": "장기요양 본인부담금, 어떻게 정해지나요",
     "memo": "재가급여 본인부담률(15%), 본인부담이 없거나 감경되는 경우(법정 기준), 급여 밖 비용은 본인 부담. 금액 예시는 쓰지 않습니다.\n자주 받는 질문: [ ]"},
    {"month": 0, "post_type": "care_guide", "title": "장기요양인정 유효기간과 갱신, 놓치지 마세요",
     "memo": "장기요양인정 유효기간(2년)과 갱신 시 등급별 유효기간.\n자주 받는 질문: [ ]"},
    {"month": 0, "post_type": "care", "title": "강서구 주간보호센터, 하루는 이렇게 흘러갑니다",
     "memo": "송영으로 시작해 프로그램(인지&신체 통합·실버노래교실·그림책·재활운동·실버미술), 식사와 간식, 위생관리, 귀가 송영까지의 하루.\n현장 이야기: [ ]"},
    {"month": 0, "post_type": "care", "title": "장기요양등급을 받았다면, 방문요양으로 집에서 돌봄 받기",
     "memo": "방문요양에서 요양보호사가 해 드리는 일(신체활동·가사 및 일상생활·정서·인지생활 지원)과 대상. 가사서비스와의 차이도 짧게.\n자주 받는 질문: [ ]"},
    {"month": 0, "post_type": "care", "title": "재활운동 특화 주간보호센터의 프로그램",
     "memo": "재활운동 특화 주간보호의 프로그램 소개. 활동 내용만 설명하고 회복·예방 효과는 단정하지 않습니다.\n프로그램 현장 이야기: [ ]"},
    {"month": 0, "post_type": "recruit_care", "title": "요양보호사 선생님을 모십니다 — 존엄케어를 함께할 분",
     "memo": "강서나눔통합돌봄센터 요양보호사 모집. 요양보호사를 전문 직업인으로 존중하는 '존엄케어'.\n모집 분야·근무 조건: [ ]"},
    {"month": 0, "post_type": "recruit", "title": "가사관리사 모집 — 경험 없어도 교육 후 시작",
     "memo": "가사관리사 모집. 경험이 없어도 지원할 수 있고 교육을 받은 뒤 근무를 시작합니다. 돌봄 종사자가 세운 협동조합에서 일한다는 것.\n모집 인원·근무 조건: [ ]"},
]

HOUSE_FEW_SHOT = [
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


# 기본(주간보호) 예시 글은 없습니다. 회사가 쓴 실제 주간보호 글이 생기면 여기에 넣으세요 —
# 지어낸 예시는 말투뿐 아니라 내용까지 따라 하게 만듭니다. 그동안은 톤앤매너가 문체를 정합니다.
FEW_SHOT_SAMPLES: list = []

# 주간보호 송영 지역(전단 기준). 동네 키워드·지역 해시태그의 기본 재료입니다.
SERVICE_AREAS = ["강서구", "화곡동", "등촌동", "가양동", "마곡동", "발산동", "우장산동", "공항동", "방화동"]

# 가사서비스 글(글 유형 [가사] …)에만 쓰는 보조 화자. 브랜드 킷의 house_voice에 저장되어 화면에서
# 고칠 수 있고, 이 값은 처음 한 번 채우는 기본값입니다 (content_writer._brand_kit_for).
HOUSE_SUB_BRAND = "우렁각시 홈서비스"
HOUSE_VOICE = {
    "sub_brand": HOUSE_SUB_BRAND,
    "persona": HOUSE_PERSONA,
    "tone_and_manner": HOUSE_TONE,
    "few_shot_samples": HOUSE_FEW_SHOT,
    "service_areas": HOUSE_SERVICE_AREAS,
}


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
        non_target_keywords=NON_TARGET_KEYWORDS,
        service_areas=SERVICE_AREAS,
        product_defaults=PRODUCT_DEFAULTS,
        care_defaults=CARE_PRODUCT_DEFAULTS,
        house_voice=HOUSE_VOICE,
        news_exclude_terms=NEWS_EXCLUDE_TERMS,
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
SEED_BLACKLIST_ADDITIONS: dict = {
    "은광회복지재단": "은강회복지재단",
    "연간 70만 원": "70만 원",
    "연 70만 원": "70만 원",
    "댁 앞까지": "댁까지",
    "집 앞까지": "댁까지",
}


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

    added += _apply_seed_field_additions(done)
    added += _apply_care_division(done)

    repo.set_app_state(_SEED_FIXES_STATE_KEY, {"done": sorted(done)})
    return applied + added


# Brand Kit fields introduced after this company's kit was first seeded. Each
# is filled once, and only while the admin's value is still empty — a field
# the admin has already set (or emptied on purpose after the first fill) is
# never touched again, the same rule SEED_BLACKLIST_ADDITIONS follows.
# 이미 시드된 브랜드 킷에 주간보호 사업 분야를 더할 때의 1회성 변경. 담당자가 손대지
# 않은 원문 그대로일 때만 바꾸고(SEED_FIXES와 같은 원칙), 추가는 없는 항목만 넣습니다.
SEED_FACT_REPLACEMENTS = [
    (
        "센터는 가사관리 외에 방문요양·장애인 활동지원·병원동행·긴급돌봄을 제공하며, 강서나눔통합돌봄센터(케어누리 강서점, 강서구 수명로2길 96 신관 2층, 02-6958-9084)에서 주간보호(월~토 08:30~18:00)와 방문요양을 운영합니다.",
        CARE_FACTS,
    ),
]
# 업종 문구 — 시드 당시 원문 그대로일 때만 주간보호를 포함한 문구로 바꿉니다.
SEED_INDUSTRY_FIX = (
    "서울 강서·양천 지역 정부인증 가사서비스(청소·세탁·정리수납) 제공기관 (고용노동부 인증 사회적기업 · 사회적협동조합)",
    INDUSTRY,
)
SEED_KEYWORD_ADDITIONS = {
    "강서구 방문요양": 2.0, "강서구 주간보호센터": 2.0, "화곡동 주간보호센터": 2.0, "강서구 데이케어센터": 2.0,
}
SEED_KEYWORD_REMOVALS = ["가사서비스 요금", "맞벌이 가사"]
SEED_AREA_ADDITIONS = ["우장산동"]


def _apply_care_division(done: set) -> int:
    kit = repo.get_brand_kit()
    changes = {}

    facts = list(kit.get("core_facts") or [])
    for old, new in SEED_FACT_REPLACEMENTS:
        marker = "facts:care-division"
        if marker in done:
            continue
        if old in facts:
            at = facts.index(old)
            facts[at:at + 1] = [f for f in new if f not in facts]
            changes["core_facts"] = facts
        done.add(marker)

    if "terminology:care-division" not in done:
        terms = dict(kit.get("terminology") or {})
        added = {k: v for k, v in CARE_TERMINOLOGY.items() if k not in terms}
        if added:
            terms.update(added)
            changes["terminology"] = terms
        done.add("terminology:care-division")

    # 데이케어센터는 주간보호 분야를 더한 뒤에 찾은 동의어라 별도 표시로 한 번 더 더합니다.
    if "keywords:daycare-synonym" not in done:
        pool = list(changes.get("seo_keywords") or kit.get("seo_keywords") or [])
        weights = dict(changes.get("keyword_weights") or kit.get("keyword_weights") or {})
        terms = dict(changes.get("terminology") or kit.get("terminology") or {})
        if "keywords:care-division" in done and "강서구 데이케어센터" not in pool:
            pool.append("강서구 데이케어센터")
            weights.setdefault("강서구 데이케어센터", 2.0)
            changes["seo_keywords"] = pool
            changes["keyword_weights"] = weights
        if "데이케어센터" not in terms:
            terms["데이케어센터"] = CARE_TERMINOLOGY["데이케어센터"]
            changes["terminology"] = terms
        done.add("keywords:daycare-synonym")

    if "keywords:care-division" not in done:
        pool = list(kit.get("seo_keywords") or [])
        weights = dict(kit.get("keyword_weights") or {})
        before = list(pool)
        pool = [k for k in pool if k not in SEED_KEYWORD_REMOVALS]
        for keyword, weight in SEED_KEYWORD_ADDITIONS.items():
            if keyword not in pool:
                pool.append(keyword)
                weights.setdefault(keyword, weight)
        if pool != before:
            changes["seo_keywords"] = pool
            changes["keyword_weights"] = {k: v for k, v in weights.items() if k in pool}
            changes["non_target_keywords"] = [k for k in (kit.get("non_target_keywords") or []) if k in pool]
        done.add("keywords:care-division")

    # 기본 화자를 주간보호로, 가사서비스는 보조 화자(house_voice)로. 지금 킷의 가사 화자는
    # (담당자가 고친 내용 포함) 그대로 house_voice로 옮기고, 기본 화자 자리는 비어 있지 않을 때만
    # 바꿉니다 — 서브 브랜드가 아직 '우렁각시 홈서비스'인 킷만 대상입니다.
    if "voice:care-primary" not in done:
        if (kit.get("sub_brand") or "").strip() == HOUSE_SUB_BRAND:
            changes["house_voice"] = {
                "sub_brand": kit.get("sub_brand"),
                "persona": kit.get("persona") or HOUSE_PERSONA,
                "tone_and_manner": kit.get("tone_and_manner") or HOUSE_TONE,
                "few_shot_samples": kit.get("few_shot_samples") or HOUSE_FEW_SHOT,
                "service_areas": kit.get("service_areas") or HOUSE_SERVICE_AREAS,
            }
            changes.update(
                sub_brand=SUB_BRAND, persona=PERSONA, tone_and_manner=TONE_AND_MANNER,
                few_shot_samples=FEW_SHOT_SAMPLES, service_areas=SERVICE_AREAS, industry=INDUSTRY,
            )
        done.add("voice:care-primary")

    # 화면 통합 — 담당자가 고치지 않은(같은 항목 집합) 팩트·용어집만 새 순서로 다시 씁니다.
    if "order:integrated" not in done:
        facts_now = list(changes.get("core_facts") or kit.get("core_facts") or [])
        if facts_now and set(facts_now) == set(CORE_FACTS):
            changes["core_facts"] = list(CORE_FACTS)
        terms_now = dict(changes.get("terminology") or kit.get("terminology") or {})
        if terms_now and terms_now == TERMINOLOGY:
            changes["terminology"] = dict(TERMINOLOGY)
        done.add("order:integrated")

    # [새로 고르기]의 '경쟁 과다(문서/검색 100)' 기준이 지역 키워드에 그대로 적용되던 동안(2026-10-03,
    # keyword_curator.LOCAL_MAX_DOCS_PER_SEARCH로 수정) 빠진 돌봄 지역 키워드를 한 번 되돌립니다. 그때
    # 들어온 키워드는 건드리지 않고, 센터 제공 여부가 확인되지 않은 '노인맞춤돌봄서비스'만 타깃에서 뺍니다.
    if "terminology:eungang" not in done:
        terms = dict(changes.get("terminology") or kit.get("terminology") or {})
        if "은강회복지재단" not in terms:
            terms["은강회복지재단"] = CARE_TERMINOLOGY["은강회복지재단"]
            changes["terminology"] = terms
        done.add("terminology:eungang")

    if "keywords:restore-local" not in done:
        pool = list(changes.get("seo_keywords") or kit.get("seo_keywords") or [])
        weights = dict(changes.get("keyword_weights") or kit.get("keyword_weights") or {})
        non_targets = list(changes.get("non_target_keywords") or kit.get("non_target_keywords") or [])
        restored = [k for k in SEED_KEYWORD_ADDITIONS if k not in pool]
        if restored:
            pool = restored + pool
            for k in restored:
                weights.setdefault(k, SEED_KEYWORD_ADDITIONS[k])
        if "노인맞춤돌봄서비스" in pool and "노인맞춤돌봄서비스" not in non_targets:
            non_targets.append("노인맞춤돌봄서비스")
        if restored or non_targets != list(kit.get("non_target_keywords") or []):
            changes.update(seo_keywords=pool, keyword_weights=weights, non_target_keywords=non_targets)
        done.add("keywords:restore-local")

    # 장기요양 제도 정보 팩트와 화자 규칙을 한 번 더합니다 (첫 가사서비스 팩트 바로 앞에).
    if "facts:ltc-info" not in done:
        facts = list(changes.get("core_facts") or kit.get("core_facts") or [])
        missing = [f for f in INFO_FACTS if f not in facts]
        if missing:
            at = next((i for i, f in enumerate(facts) if f in HOUSE_FACTS), len(facts))
            facts[at:at] = missing
            changes["core_facts"] = facts
        tone = changes.get("tone_and_manner") or kit.get("tone_and_manner") or ""
        if INFO_TONE_RULE not in tone:
            changes["tone_and_manner"] = tone.rstrip() + "\n- " + INFO_TONE_RULE
        done.add("facts:ltc-info")

    if "industry:care-division" not in done:
        old, new = SEED_INDUSTRY_FIX
        if (kit.get("industry") or "").strip() == old and "industry" not in changes:
            changes["industry"] = new
        done.add("industry:care-division")

    if "care-defaults:care-division" not in done:
        if not kit.get("care_defaults"):
            changes["care_defaults"] = CARE_PRODUCT_DEFAULTS
        done.add("care-defaults:care-division")

    if "areas:care-division" not in done:
        areas = list(kit.get("service_areas") or [])
        missing = [a for a in SEED_AREA_ADDITIONS if a not in areas]
        if areas and missing and "service_areas" not in changes:
            changes["service_areas"] = areas + missing
        done.add("areas:care-division")

    if changes:
        repo.save_brand_kit(**changes)
    return len(changes)


def _seed_field_additions() -> dict:
    return {
        "service_areas": SERVICE_AREAS,
        "product_defaults": PRODUCT_DEFAULTS,
        "news_exclude_terms": NEWS_EXCLUDE_TERMS,
    }


def _apply_seed_field_additions(done: set) -> int:
    kit = repo.get_brand_kit()
    changes = {}
    for field, value in _seed_field_additions().items():
        marker = f"field:{field}"
        if marker in done:
            continue
        if not kit.get(field) and value:
            changes[field] = value
        done.add(marker)

    # Non-target keywords are added per keyword, and only when the keyword is
    # in the pool — an admin who removed '가사관리사' from the pool keeps it out.
    non_targets = list(kit.get("non_target_keywords") or [])
    pool = kit.get("seo_keywords") or []
    for keyword in NON_TARGET_KEYWORDS:
        marker = f"non_target:{keyword}"
        if marker in done:
            continue
        if keyword in pool and keyword not in non_targets:
            non_targets.append(keyword)
            changes["non_target_keywords"] = non_targets
        done.add(marker)

    if changes:
        repo.save_brand_kit(**changes)
    return len(changes)
