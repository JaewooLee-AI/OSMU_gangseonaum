"""브랜드 킷.

Business rules (carried over from the original Streamlit screen):
- a blank SEO-keyword weight cell means "no opinion yet" -> neutral 1.0, not 0
- a blank "검색 타깃" checkbox means still included, not excluded
- a keyword-competitiveness freshness warning must stay visible, since
  expiry silently turns off conversion weighting (ai_workers.keyword_research)
- the brand kit is pre-seeded on first launch (core/brand_seed.py), so this
  view never actually starts from an empty state
"""
from __future__ import annotations

import flet as ft

from ai_workers import content_mode, fact_freshness, factsheet, keyword_research
from ai_workers.content_writer import SNS_CHANNELS, enabled_channels
from core import repo

from flet_app.components.editable_table import ColumnSpec, EditableTable
from flet_app.state import AppState
from flet_app.theme import BRAND_COLORS, fs, palette_row

FEW_SHOT_DELIMITER = "\n---\n"


def build(page: ft.Page, state: AppState) -> ft.Control:
    scale = state.font_scale
    existing = repo.get_brand_kit()

    # --- 기업 · 채널 ---------------------------------------------------------
    brand_name = ft.TextField(label="기업명", value=existing.get("brand_name") or "", expand=True)
    sub_brand = ft.TextField(label="돌봄센터 브랜드명", value=existing.get("sub_brand") or "", expand=True)
    industry = ft.TextField(label="업종", value=existing.get("industry") or "", expand=True)
    homepage = ft.TextField(label="홈페이지", value=existing.get("homepage") or "", expand=True)
    naver_blog_id = ft.TextField(
        label="네이버 블로그 아이디",
        value=existing.get("naver_blog_id") or "",
        helper="blog.naver.com/<아이디>. 반자동 게시가 이 블로그로 글을 올립니다.",
        expand=True,
    )
    instagram_handle = ft.TextField(
        label="인스타그램 핸들", value=existing.get("instagram_handle") or "", expand=True
    )

    guardrail_enabled = ft.Switch(
        label="🛡️ 표시·광고 컴플라이언스 가드레일",
        value=bool(existing.get("guardrail_enabled", True)),
    )

    persona = ft.TextField(
        label="브랜드 페르소나 (기본 화자 — 주간보호·방문요양)",
        value=existing.get("persona") or "",
        multiline=True,
        min_lines=4,
        max_lines=8,
        expand=True,
    )
    tone_and_manner = ft.TextField(
        label="톤앤매너 가이드 (기본 화자)",
        value=existing.get("tone_and_manner") or "",
        multiline=True,
        min_lines=6,
        max_lines=12,
        expand=True,
    )

    # --- 핵심 팩트 ------------------------------------------------------------
    core_facts_field = ft.TextField(
        label="핵심 팩트 (한 줄에 하나씩)",
        value="\n".join(existing.get("core_facts") or []),
        multiline=True,
        min_lines=8,
        max_lines=16,
        expand=True,
    )

    # --- 용어집 ---------------------------------------------------------------
    terminology = existing.get("terminology") or {}
    terminology_table = EditableTable(
        columns=[
            ColumnSpec("term", "용어", "text"),
            ColumnSpec("desc", "설명/올바른 표기", "text"),
        ],
        rows=[{"term": k, "desc": v} for k, v in terminology.items()],
    )

    # --- 기본 콘텐츠 모드 -------------------------------------------------------
    mode_keys = content_mode.ORDER
    saved_mode = existing.get("default_content_mode") or content_mode.DEFAULT_MODE
    mode_dropdown = ft.Dropdown(
        label="기본 콘텐츠 모드",
        expand=True,
        value=saved_mode if saved_mode in mode_keys else content_mode.DEFAULT_MODE,
        options=[
            ft.DropdownOption(key=k, text=f"{content_mode.MODES[k]['icon']} {content_mode.MODES[k]['label']}")
            for k in mode_keys
        ],
    )
    mode_captions = ft.Column(
        [
            ft.Text(
                f"· {content_mode.MODES[k]['icon']} {content_mode.MODES[k]['label']} — "
                f"{content_mode.describe(k)}",
                size=fs(12, scale),
                color=BRAND_COLORS["text_muted"],
            )
            for k in mode_keys
        ]
    )

    # --- SEO 키워드 -----------------------------------------------------------
    keyword_weights = existing.get("keyword_weights") or {}
    non_target = set(existing.get("non_target_keywords") or [])
    keywords_table = EditableTable(
        columns=[
            ColumnSpec("keyword", "키워드", "text"),
            ColumnSpec("weight", "전환 가중치", "number", default=1.0, width=90),
            ColumnSpec("target", "검색 타깃", "checkbox", default=True),
        ],
        rows=[
            {
                "keyword": k,
                "weight": float(keyword_weights.get(k, 1.0)),
                "target": k not in non_target,
            }
            for k in (existing.get("seo_keywords") or [])
        ],
    )

    # 만료는 조용히 일어나고, 조용히 가중치 체계를 끕니다 — keyword_research.pool_freshness 참고.
    freshness = keyword_research.pool_freshness(existing.get("seo_keywords") or [])
    freshness_banner: ft.Control | None = None
    if freshness["stale"]:
        stale = freshness["stale"]
        freshness_banner = ft.Container(
            content=ft.Text(
                f"📉 경쟁도 측정이 만료된 키워드 {len(stale)}개: "
                f"{', '.join(stale[:6])}{'…' if len(stale) > 6 else ''}\n"
                "만료된 키워드는 전환 가중치가 적용되지 않고, 초안에 몇 번 나왔는지로만 순위가 "
                "정해집니다. ⚙️ 설정 페이지에서 재측정하세요.",
                color="#B3261E",
                size=fs(12, scale),
            ),
            bgcolor="#FDECEA",
            padding=10,
            border_radius=8,
        )
    elif freshness["days_left"] is not None:
        freshness_banner = ft.Text(
            f"📈 경쟁도 측정: 가장 오래된 것이 {freshness['oldest_document_age']:.0f}일 전 · "
            f"{freshness['days_left']:.0f}일 후 만료됩니다. 만료되면 전환 가중치가 조용히 꺼지므로, "
            "그 전에 ⚙️ 설정에서 재측정하세요.",
            size=fs(12, scale),
            color=BRAND_COLORS["text_muted"],
        )

    # --- 금기어 사전 -----------------------------------------------------------
    blacklist_map = existing.get("blacklist_map") or {}
    blacklist_table = EditableTable(
        columns=[
            ColumnSpec("bad", "금기어", "text"),
            ColumnSpec("good", "치환어", "text"),
        ],
        rows=[{"bad": k, "good": v} for k, v in blacklist_map.items()],
    )

    # --- Few-shot 샘플 ----------------------------------------------------------
    few_shot_field = ft.TextField(
        label="예시 글 (여러 개면 빈 줄에 --- 로 구분)",
        value=FEW_SHOT_DELIMITER.join(existing.get("few_shot_samples") or []),
        multiline=True,
        min_lines=8,
        max_lines=16,
        expand=True,
    )

    # --- 가사서비스 보조 화자 -------------------------------------------------
    house = existing.get("house_voice") or {}
    house_sub = ft.TextField(label="가사서비스 브랜드명", value=house.get("sub_brand") or "", expand=True)
    house_persona = ft.TextField(
        label="가사서비스 글 페르소나", value=house.get("persona") or "",
        multiline=True, min_lines=3, max_lines=8, expand=True,
    )
    house_tone = ft.TextField(
        label="가사서비스 글 톤앤매너", value=house.get("tone_and_manner") or "",
        multiline=True, min_lines=5, max_lines=12, expand=True,
    )
    house_areas = ft.TextField(
        label="가사서비스 지역 (쉼표로 구분)", value=", ".join(house.get("service_areas") or []), expand=True,
    )

    # --- 서비스 지역 · 서비스 기본값 · 채널 · 뉴스 제외어 -------------------------
    service_areas_field = ft.TextField(
        label="서비스 지역 (쉼표로 구분)",
        value=", ".join(existing.get("service_areas") or []),
        helper="동네 키워드 후보(🔑 SEO 키워드)와 인스타·당근 지역 표현의 재료입니다. 실제로 서비스하는 곳만 적으세요.",
        expand=True,
    )
    defaults = existing.get("product_defaults") or {}
    default_fields = {
        key: ft.TextField(label=label, value=defaults.get(key) or "", hint_text=placeholder, expand=True)
        for key, label, placeholder in factsheet.PRODUCT.fields
    }
    default_rows = []
    keys = list(default_fields)
    for i in range(0, len(keys), 2):
        default_rows.append(ft.Row([default_fields[k] for k in keys[i:i + 2]]))

    care_saved = existing.get("care_defaults") or {}
    care_fields = {
        key: ft.TextField(label=label, value=care_saved.get(key) or "", expand=True)
        for key, label, _ in factsheet.PRODUCT.fields
    }
    care_rows = []
    for i in range(0, len(keys), 2):
        care_rows.append(ft.Row([care_fields[k] for k in keys[i:i + 2]]))

    active_channels = set(enabled_channels(existing))
    channel_checks = {
        key: ft.Checkbox(label=label, value=key in active_channels) for key, label in SNS_CHANNELS.items()
    }
    news_exclude_field = ft.TextField(
        label="뉴스 큐레이션 제외어 (쉼표로 구분)",
        value=", ".join(existing.get("news_exclude_terms") or []),
        helper="기사 제목·요약에 이 말이 있으면 뉴스 검색 결과에서 뺍니다 (띄어쓰기 무시).",
        expand=True,
    )

    freshness_note = fact_freshness.summary(existing)
    fact_banner = ft.Container(
        content=ft.Text(freshness_note, color="#8A6D3B", size=fs(12, scale)),
        bgcolor="#FFF6E5", padding=10, border_radius=8, visible=bool(freshness_note),
    )

    # --- 저장 --------------------------------------------------------------
    save_status = ft.Text("", size=fs(12, scale), color="#1B6E3C")
    guardrail_warning_box = ft.Container(visible=not bool(existing.get("guardrail_enabled", True)))
    guardrail_warning_box.content = ft.Text(
        "가드레일이 꺼져 있습니다. 결과 보장·요금 오표시·인증 확대 같은 표현이 검수 없이 발행될 수 있습니다.",
        color="#B3261E",
        size=fs(12, scale),
    )
    guardrail_warning_box.bgcolor = "#FDECEA"
    guardrail_warning_box.padding = 10
    guardrail_warning_box.border_radius = 8

    def on_save(e: ft.Event) -> None:
        core_facts = [line.strip() for line in (core_facts_field.value or "").splitlines() if line.strip()]
        few_shot_samples = [
            s.strip() for s in (few_shot_field.value or "").split(FEW_SHOT_DELIMITER.strip()) if s.strip()
        ]

        new_terminology = {
            row["term"]: row["desc"] for row in terminology_table.get_rows() if row["term"]
        }
        new_blacklist = {
            row["bad"]: row["good"] for row in blacklist_table.get_rows() if row["bad"]
        }

        new_keywords: list[str] = []
        new_weights: dict[str, float] = {}
        new_non_targets: list[str] = []
        for row in keywords_table.get_rows():
            kw = row["keyword"]
            if not kw or kw in new_weights:
                continue
            new_keywords.append(kw)
            new_weights[kw] = row["weight"]
            if not row["target"]:
                new_non_targets.append(kw)

        repo.save_brand_kit(
            brand_name=brand_name.value,
            sub_brand=sub_brand.value,
            industry=industry.value,
            homepage=homepage.value,
            naver_blog_id=naver_blog_id.value,
            instagram_handle=instagram_handle.value,
            guardrail_enabled=guardrail_enabled.value,
            persona=persona.value,
            tone_and_manner=tone_and_manner.value,
            core_facts=core_facts,
            terminology=new_terminology,
            seo_keywords=new_keywords,
            keyword_weights=new_weights,
            non_target_keywords=new_non_targets,
            default_content_mode=mode_dropdown.value,
            blacklist_map=new_blacklist,
            few_shot_samples=few_shot_samples,
            service_areas=[a.strip() for a in (service_areas_field.value or "").split(",") if a.strip()],
            product_defaults={k: tf.value.strip() for k, tf in default_fields.items() if (tf.value or "").strip()},
            care_defaults={k: tf.value.strip() for k, tf in care_fields.items() if (tf.value or "").strip()},
            news_exclude_terms=[t.strip() for t in (news_exclude_field.value or "").split(",") if t.strip()],
            enabled_channels=[k for k, cb in channel_checks.items() if cb.value],
            house_voice={
                **house,
                "sub_brand": house_sub.value.strip(),
                "persona": house_persona.value.strip(),
                "tone_and_manner": house_tone.value.strip(),
                "service_areas": [a.strip() for a in (house_areas.value or "").split(",") if a.strip()],
            },
        )
        fact_banner.content.value = fact_freshness.summary(repo.get_brand_kit())
        fact_banner.visible = bool(fact_banner.content.value)

        guardrail_warning_box.visible = not guardrail_enabled.value
        save_status.value = (
            f"✅ 저장했습니다. (핵심 팩트 {len(core_facts)} · 용어 {len(new_terminology)} · "
            f"SEO 키워드 {len(new_keywords)} · 금기어 {len(new_blacklist)} · 샘플 {len(few_shot_samples)})"
        )
        page.update()

    save_button = ft.FilledButton("저장", icon=ft.Icons.SAVE, on_click=on_save)

    # --- 제목 반복 방지 (Streamlit에선 "폼 밖" 제약이 있었지만 Flet엔 없음) -------
    history_count = repo.title_history_count()
    history_list = ft.Column(
        [ft.Text(f"• {t}", size=fs(12, scale)) for t in repo.recent_titles(50)],
        scroll=ft.ScrollMode.AUTO,
        height=200,
        visible=False,
    )

    def toggle_history(e: ft.Event) -> None:
        history_list.visible = not history_list.visible
        page.update()

    def clear_history(e: ft.Event) -> None:
        repo.clear_title_history()
        history_list.controls = []
        save_status.value = "제목 이력을 삭제했습니다."
        page.update()

    history_section = ft.Column(
        [
            ft.Text("🎲 제목 반복 방지", weight=ft.FontWeight.BOLD),
            ft.Text(
                f"지금까지 생성한 제목 {history_count}건을 기억해, 새 제목이 과거 제목과 문장 구조까지 "
                "겹치면 자동으로 다시 짓습니다. 이 이력은 캠페인을 삭제해도 남습니다.",
                size=fs(12, scale),
                color=BRAND_COLORS["text_muted"],
            ),
            ft.Row(
                [
                    ft.TextButton(f"이력 {history_count}건 보기/숨기기", on_click=toggle_history),
                    ft.TextButton("🗑️ 제목 이력 전체 삭제", on_click=clear_history),
                ]
            ),
            history_list,
        ]
    )

    def section(title: str, subtitle: str, color: str) -> ft.Control:
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=fs(16, scale), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(subtitle, size=fs(11, scale), color=ft.Colors.WHITE),
            ], spacing=2),
            bgcolor=color, padding=ft.Padding.symmetric(horizontal=14, vertical=10), border_radius=8,
        )

    def note(text: str) -> ft.Control:
        return ft.Text(text, size=fs(11, scale), color=BRAND_COLORS["text_muted"])

    # 한 화면에 법인 하나, 사업 둘. 화자(페르소나·톤·지역·기본값)는 사업마다 따로 두고 — 전화번호와
    # 일하는 사람의 호칭이 달라, 하나로 섞은 실측 글은 주간보호 글이 가사 번호로 끝났습니다 — 팩트·용어집·
    # 키워드·금기어는 법인 공통 자료로 한 번만 둡니다.
    return ft.Column(
        [
            ft.Text("브랜드 킷", size=fs(24, scale), weight=ft.FontWeight.BOLD),
            note("여기 등록한 내용은 매 생성마다 프롬프트에 그대로 주입됩니다 (유사도 검색이 아니라 전체 주입). "
                 "저장 버튼은 화면 맨 아래에 있습니다."),
            guardrail_warning_box,

            section("🏢 법인 공통 — 사회적협동조합 강서나눔돌봄센터",
                    "두 사업이 함께 쓰는 법인 정보와 채널입니다.", BRAND_COLORS["primary_dark"]),
            ft.Text("🎨 브랜드 컬러", weight=ft.FontWeight.BOLD),
            palette_row(scale=scale),
            ft.Row([brand_name]),
            industry,
            ft.Row([homepage, naver_blog_id, instagram_handle]),
            guardrail_enabled,

            section("🧓 돌봄센터 — 주간보호·방문요양 (주력 · 기본 화자)",
                    "SNS 강화의 대상 사업입니다. 글 유형 [돌봄]·공지·자유 글이 이 화자로 쓰입니다.",
                    BRAND_COLORS["primary"]),
            sub_brand,
            persona,
            tone_and_manner,
            ft.Text("📍 서비스 지역 (주간보호 송영 지역)", weight=ft.FontWeight.BOLD),
            service_areas_field,
            ft.Text("🧾 서비스·이용 정보 기본값", weight=ft.FontWeight.BOLD),
            note("글 유형 [돌봄]이 이 값을 씁니다. 비용(요금)은 고객 확인 전이라 비워 두었습니다. "
                 "채운 값은 그 글에 '반드시 들어갈 사실'로 전달되므로 확인된 내용만 적으세요."),
            *care_rows,

            section("🧹 가사서비스 — 우렁각시 홈서비스 (보조 화자)",
                    "글 유형 [가사] …를 고른 글에만 쓰입니다.", BRAND_COLORS["secondary"]),
            house_sub,
            house_persona,
            house_tone,
            house_areas,
            ft.Text("🧾 서비스·이용 정보 기본값", weight=ft.FontWeight.BOLD),
            note("글 유형 [가사]와 워크벤치 [📥 브랜드 킷 기본값 채우기]가 이 값을 씁니다."),
            *default_rows,

            section("📚 공통 자료 — 두 사업이 함께 쓰는 사실·표기·키워드",
                    "모든 글과 컴플라이언스 검수에 전부 들어갑니다.", BRAND_COLORS["text"]),
            ft.Text("🏭 회사 핵심 팩트 (법인 공통 → 돌봄센터 → 가사서비스 순)", weight=ft.FontWeight.BOLD),
            fact_banner,
            core_facts_field,
            ft.Text("📖 회사 용어집", weight=ft.FontWeight.BOLD),
            terminology_table.build(),
            ft.Text("🔍 SEO 키워드 (네이버 블로그 전용)", weight=ft.FontWeight.BOLD),
            note("🎯 '검색 타깃'을 끈 키워드는 본문에는 써도 글의 노림·제목 키워드로는 고르지 않습니다. "
                 "꼭 쓰는 호칭(가사관리사)이나 제공 여부가 확인되지 않은 말(노인맞춤돌봄서비스)이 여기에 해당합니다."),
            keywords_table.build(),
            *([freshness_banner] if freshness_banner else []),
            mode_dropdown,
            mode_captions,
            ft.Text("📣 함께 만들 채널", weight=ft.FontWeight.BOLD),
            note("네이버 블로그 본문과 발행 태그는 항상 만듭니다. 운영하지 않는 채널을 끄면 생성이 빨라지고 "
                 "그 채널의 AI 호출(작성 + 검수)이 0이 됩니다."),
            ft.Row(list(channel_checks.values()), wrap=True),
            ft.Text("📰 뉴스 큐레이션 제외어", weight=ft.FontWeight.BOLD),
            news_exclude_field,
            ft.Text("🚫 금기어 치환 사전 (과장·오인 광고 방지)", weight=ft.FontWeight.BOLD),
            blacklist_table.build(),
            ft.Text("✍️ 기본 화자(돌봄센터) 예시 글", weight=ft.FontWeight.BOLD),
            note("회사가 실제로 쓴 주간보호 글이 생기면 넣으세요. 지어낸 예시는 말투뿐 아니라 내용까지 따라 하게 만듭니다."),
            few_shot_field,
            ft.Row([save_button, save_status]),
            ft.Divider(),
            history_section,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10,
    )
