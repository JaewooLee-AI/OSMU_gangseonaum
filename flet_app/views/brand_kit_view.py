"""브랜드 킷.

킷은 사업 분야마다 하나씩 둡니다 — 처음에는 '돌봄센터(주간보호·방문요양)'와
'가사서비스(우렁각시 홈서비스)' 두 개이고, 필요하면 더 만들 수 있습니다. 화면은 세 부분입니다:
- 킷 목록: 새로 만들기(기존 킷 복사) · 복제 · 이름 변경 · 삭제 · 되살리기.
  삭제는 보관(숨김)이라 글에 남은 킷 연결이 끊기지 않습니다 — core/repo.archive_brand_kit.
- 고른 킷 편집: 브랜드명·페르소나·톤·서비스 지역·기본값·팩트·용어집·SEO 키워드처럼 사업마다 다른 값.
- 회사 공통: 기업명·계정·금기어·가드레일·뉴스 제외어·생성 채널처럼 어느 킷으로 쓰든 같은 값.

Business rules (carried over from the original Streamlit screen):
- a blank SEO-keyword weight cell means "no opinion yet" -> neutral 1.0, not 0
- a blank "검색 타깃" checkbox means still included, not excluded
- a keyword-competitiveness freshness warning must stay visible, since
  expiry silently turns off conversion weighting (ai_workers.keyword_research)
- the brand kits are pre-seeded on first launch (core/brand_seed.py), so this
  view never actually starts from an empty state
"""
from __future__ import annotations

import flet as ft

from ai_workers import content_mode, fact_freshness, factsheet, formatting, keyword_research
from ai_workers.content_writer import SNS_CHANNELS, enabled_channels
from core import repo

from flet_app.components.editable_table import ColumnSpec, EditableTable
from flet_app.state import AppState
from flet_app.theme import BRAND_COLORS, fs, palette_row

FEW_SHOT_DELIMITER = "\n---\n"


def build(page: ft.Page, state: AppState) -> ft.Control:
    root = ft.Container(expand=True)

    def render() -> None:
        root.content = _build_screen(page, state, render)
        root.update()

    root.content = _build_screen(page, state, render)
    return root


def _snack(page: ft.Page, text: str) -> None:
    page.show_dialog(ft.SnackBar(ft.Text(text)))


def _name_dialog(page: ft.Page, title: str, initial: str, ok_label: str, on_ok, note: str = "") -> None:
    """이름 하나를 받는 대화상자. `on_ok(name)`이 repo.BrandKitError를 내면 창을 닫지 않고 그 문장을 보여줍니다."""
    field = ft.TextField(label="킷 이름", value=initial, autofocus=True, width=360)
    error = ft.Text("", color="#B3261E", size=12)

    def submit(e: ft.Event) -> None:
        try:
            on_ok(field.value or "")
        except repo.BrandKitError as exc:
            error.value = str(exc)
            error.update()
            return
        page.pop_dialog()

    field.on_submit = submit
    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Column(
            [*([ft.Text(note, size=12, color=BRAND_COLORS["text_muted"])] if note else []), field, error],
            tight=True, spacing=8,
        ),
        actions=[
            ft.TextButton("취소", on_click=lambda e: page.pop_dialog()),
            ft.FilledButton(ok_label, on_click=submit),
        ],
    ))


def _archive_dialog(page: ft.Page, kit: dict, others: list[dict], on_done) -> None:
    """킷 삭제(보관) 확인. 아직 게시하지 않은 글이 이 킷을 쓰면, 다른 킷으로 옮길지 고르게 합니다."""
    unpublished = repo.count_campaigns_using_kit(kit["id"])
    move_choice = [None]
    body: list[ft.Control] = [ft.Text(
        f"'{kit['name']}' 킷을 삭제할까요? 삭제한 킷은 이 화면 아래 '삭제한 킷'에서 언제든 되살릴 수 있습니다. "
        "이미 쓴 글에는 킷 이름이 그대로 남습니다.",
        size=13,
    )]
    if kit.get("kit_key"):
        body.append(ft.Text(
            "이 킷은 회사 자료로 만든 기본 킷입니다. 삭제하면 이 사업의 글 유형과 추천 주제가 기본 킷으로 연결됩니다.",
            size=12, color="#8A6D3B",
        ))
    confirm = ft.FilledButton("삭제", bgcolor="#B3261E", color=ft.Colors.WHITE)

    if unpublished:
        keep_key = "keep"
        choice = ft.Dropdown(
            label="아직 게시하지 않은 글을…",
            width=360,
            options=[ft.DropdownOption(key=str(k["id"]), text=f"'{k['name']}' 킷으로 옮기기") for k in others]
            + [ft.DropdownOption(key=keep_key, text="옮기지 않기 (이 킷으로 계속 다시 생성할 수 있음)")],
        )

        def on_choice(e: ft.Event) -> None:
            move_choice[0] = None if choice.value == keep_key else int(choice.value)
            confirm.disabled = not choice.value
            confirm.update()

        choice.on_select = on_choice
        confirm.disabled = True
        body += [
            ft.Text(
                f"⚠️ 아직 게시하지 않은 글 {unpublished}개가 이 킷을 씁니다. 다른 킷으로 옮길지 골라주세요. "
                "옮긴 글은 다음에 생성할 때부터 새 킷을 씁니다(이미 만든 초안은 그대로).",
                size=12, color="#8A6D3B",
            ),
            choice,
        ]
    error = ft.Text("", color="#B3261E", size=12)
    body.append(error)

    def do_archive(e: ft.Event) -> None:
        try:
            moved = repo.archive_brand_kit(kit["id"], move_unpublished_to=move_choice[0])
        except repo.BrandKitError as exc:
            error.value = str(exc)
            error.update()
            return
        page.pop_dialog()
        on_done(moved)

    confirm.on_click = do_archive
    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text("브랜드 킷 삭제"),
        content=ft.Column(body, tight=True, spacing=8, width=420),
        actions=[ft.TextButton("취소", on_click=lambda e: page.pop_dialog()), confirm],
    ))


def _build_kit_list(page: ft.Page, state: AppState, render, scale: float, kits: list[dict],
                    archived: list[dict], kit_id: int) -> ft.Control:
    def select(target: int) -> None:
        state.editing_brand_kit_id = target
        render()

    def on_new(e: ft.Event) -> None:
        source_dd = ft.Dropdown(
            label="어느 킷을 복사해 시작할까요?",
            width=380,
            value=str(kit_id),
            options=[ft.DropdownOption(key=str(k["id"]), text=f"📄 '{k['name']}' 킷 복사") for k in kits],
        )
        name_field = ft.TextField(label="킷 이름", value=repo.unique_kit_name("새 킷"), autofocus=True, width=380)
        error = ft.Text("", color="#B3261E", size=12)

        def submit(ev: ft.Event) -> None:
            try:
                new_id = repo.create_brand_kit(name_field.value or "", copy_from=int(source_dd.value))
            except repo.BrandKitError as exc:
                error.value = str(exc)
                error.update()
                return
            page.pop_dialog()
            select(new_id)
            _snack(page, f"'{name_field.value.strip()}' 킷을 만들었습니다. 복사한 내용이니 이 분야에 맞게 고쳐주세요.")

        name_field.on_submit = submit
        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("새 브랜드 킷"),
            content=ft.Column(
                [
                    ft.Text(
                        "새 사업 분야를 시작할 때 씁니다. 가장 가까운 킷을 복사한 뒤 페르소나·팩트·SEO 키워드를 "
                        "그 분야에 맞게 고치세요.",
                        size=12, color=BRAND_COLORS["text_muted"],
                    ),
                    source_dd,
                    name_field,
                    error,
                ],
                tight=True, spacing=8, width=400,
            ),
            actions=[
                ft.TextButton("취소", on_click=lambda ev: page.pop_dialog()),
                ft.FilledButton("만들기", on_click=submit),
            ],
        ))

    def on_duplicate(kit: dict) -> None:
        def create(name: str) -> None:
            select(repo.create_brand_kit(name, copy_from=kit["id"]))
            _snack(page, f"'{kit['name']}' 킷을 복제했습니다.")

        _name_dialog(page, f"'{kit['name']}' 킷 복제", repo.unique_kit_name(f"{kit['name']} 복사본"), "복제", create)

    def on_rename(kit: dict) -> None:
        def rename(name: str) -> None:
            repo.save_brand_kit(kit["id"], name=name)
            render()

        _name_dialog(
            page, "킷 이름 변경", kit["name"], "변경", rename,
            note="이미 쓴 글에는 그 글을 생성할 때의 이름이 남습니다.",
        )

    def on_archive(kit: dict) -> None:
        if len(kits) <= 1:
            _snack(page, "마지막 남은 브랜드 킷은 삭제할 수 없습니다. 새 킷을 먼저 만들어주세요.")
            return

        def done(moved: int) -> None:
            if state.editing_brand_kit_id == kit["id"]:
                state.editing_brand_kit_id = None
            render()
            _snack(page, f"'{kit['name']}' 킷을 삭제했습니다." + (f" 글 {moved}개를 옮겼습니다." if moved else ""))

        _archive_dialog(page, kit, [k for k in kits if k["id"] != kit["id"]], done)

    def on_restore(kit: dict) -> None:
        name = repo.restore_brand_kit(kit["id"])
        state.editing_brand_kit_id = kit["id"]
        render()
        _snack(page, f"'{name}' 킷을 되살렸습니다.")

    rows: list[ft.Control] = []
    for i, kit in enumerate(kits):
        selected = kit["id"] == kit_id
        tag = "기본 · SNS 강화 대상" if kit.get("kit_key") == "care" else ("기본 킷" if i == 0 else "")
        rows.append(ft.Container(
            content=ft.Row(
                [
                    ft.Text(kit["name"], weight=ft.FontWeight.BOLD, size=fs(14, scale), expand=True),
                    *([ft.Text(tag, size=fs(11, scale), color=BRAND_COLORS["text_muted"])] if tag else []),
                    ft.Text("✏️ 편집 중", size=fs(12, scale), color=BRAND_COLORS["primary"]) if selected
                    else ft.TextButton("편집", on_click=lambda e, k=kit: select(k["id"])),
                    ft.TextButton("📄 복제", on_click=lambda e, k=kit: on_duplicate(k)),
                    ft.TextButton("이름 변경", on_click=lambda e, k=kit: on_rename(k)),
                    ft.TextButton("🗑️ 삭제", on_click=lambda e, k=kit: on_archive(k)),
                ],
            ),
            bgcolor=BRAND_COLORS["mint"] if selected else ft.Colors.WHITE,
            border=ft.Border.all(1, "#14000000"),
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
        ))

    controls: list[ft.Control] = [
        ft.Text("🧵 킷 목록", weight=ft.FontWeight.BOLD),
        ft.Text(
            "사업마다 킷을 두고, 워크벤치에서 글마다 어느 킷으로 쓸지 고릅니다. 주간보호·방문요양 글은 돌봄센터 킷, "
            "가사서비스 글은 가사서비스 킷으로 쓰세요 — 다른 킷을 고르면 그 사업의 화자·전화번호·팩트가 섞입니다.",
            size=fs(12, scale), color=BRAND_COLORS["text_muted"],
        ),
        *rows,
        ft.Row([ft.OutlinedButton("➕ 새 킷 만들기", on_click=on_new)]),
    ]
    if archived:
        controls.append(ft.ExpansionTile(
            title=ft.Text(f"삭제한 킷 {len(archived)}개", size=fs(13, scale)),
            controls=[
                ft.Row([
                    ft.Text(k["name"], expand=True, size=fs(13, scale)),
                    ft.TextButton("↩️ 되살리기", on_click=lambda e, k=k: on_restore(k)),
                ])
                for k in archived
            ],
        ))
    return ft.Column(controls, spacing=6)


def _split(text: str | None) -> list[str]:
    return [t.strip() for t in (text or "").split(",") if t.strip()]


def _build_screen(page: ft.Page, state: AppState, render) -> ft.Control:
    scale = state.font_scale
    kits = repo.list_brand_kits()
    archived = [k for k in repo.list_brand_kits(include_archived=True) if k.get("is_archived")]
    active_ids = {k["id"] for k in kits}
    kit_id = state.editing_brand_kit_id if state.editing_brand_kit_id in active_ids else kits[0]["id"]
    state.editing_brand_kit_id = kit_id
    existing = repo.get_brand_kit(kit_id)
    kit_name = existing.get("name") or ""

    def note(text: str) -> ft.Control:
        return ft.Text(text, size=fs(11, scale), color=BRAND_COLORS["text_muted"])

    def section(title: str, subtitle: str, color: str) -> ft.Control:
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=fs(16, scale), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(subtitle, size=fs(11, scale), color=ft.Colors.WHITE),
            ], spacing=2),
            bgcolor=color, padding=ft.Padding.symmetric(horizontal=14, vertical=10), border_radius=8,
        )

    # --- 킷: 브랜드 · 화자 ------------------------------------------------------
    sub_brand = ft.TextField(
        label="브랜드명 (이 킷의 글에 쓰는 이름)", value=existing.get("sub_brand") or "", expand=True,
        helper="예: 강서나눔통합돌봄센터 / 우렁각시 홈서비스. 당근·X 미리보기 이름에도 쓰입니다.",
    )
    industry = ft.TextField(
        label="업종 · 사업 분야", value=existing.get("industry") or "", expand=True,
        helper="이 킷이 다루는 분야. 키워드 추천과 글의 배경 설명에 쓰입니다.",
    )
    persona = ft.TextField(
        label="브랜드 페르소나 (글을 쓰는 화자)", value=existing.get("persona") or "",
        multiline=True, min_lines=4, max_lines=8, expand=True,
    )
    tone_and_manner = ft.TextField(
        label="톤앤매너 가이드", value=existing.get("tone_and_manner") or "",
        multiline=True, min_lines=6, max_lines=12, expand=True,
    )
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
    keys = list(default_fields)
    default_rows = [ft.Row([default_fields[k] for k in keys[i:i + 2]]) for i in range(0, len(keys), 2)]

    # --- 핵심 팩트 · 용어집 ----------------------------------------------------------
    core_facts_field = ft.TextField(
        label="핵심 팩트 (한 줄에 하나씩)",
        value="\n".join(existing.get("core_facts") or []),
        multiline=True, min_lines=8, max_lines=16, expand=True,
    )
    fact_note = fact_freshness.summary(existing)
    fact_banner = ft.Container(
        content=ft.Text(fact_note, color="#8A6D3B", size=fs(12, scale)),
        bgcolor="#FFF6E5", padding=10, border_radius=8, visible=bool(fact_note),
    )
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
    mode_captions = ft.Column([
        ft.Text(
            f"· {content_mode.MODES[k]['icon']} {content_mode.MODES[k]['label']} — {content_mode.describe(k)}",
            size=fs(12, scale), color=BRAND_COLORS["text_muted"],
        )
        for k in mode_keys
    ])

    # --- 원고 서식 ------------------------------------------------------------
    design_template = ft.Dropdown(
        label="서식 템플릿", width=220,
        value=existing.get("design_template") if existing.get("design_template") in formatting.TEMPLATES
        else formatting.DEFAULT_TEMPLATE,
        options=[ft.DropdownOption(key=k, text=formatting.TEMPLATES[k]["label"]) for k in formatting.TEMPLATE_ORDER],
    )
    design_strength = ft.Dropdown(
        label="서식 강도 (기본값)", width=220,
        value=existing.get("design_strength") if existing.get("design_strength") in formatting.STRENGTHS
        else formatting.DEFAULT_STRENGTH,
        options=[ft.DropdownOption(key=k, text=formatting.STRENGTHS[k]["label"]) for k in formatting.STRENGTH_ORDER],
    )
    design_captions = ft.Column(
        [ft.Text(f"· {formatting.TEMPLATES[k]['label']} — {formatting.TEMPLATES[k]['desc']}", size=fs(12, scale),
                 color=BRAND_COLORS["text_muted"]) for k in formatting.TEMPLATE_ORDER]
        + [ft.Text("· 강도: " + " / ".join(f"{formatting.STRENGTHS[k]['label']} — {formatting.STRENGTHS[k]['desc']}"
                                          for k in formatting.STRENGTH_ORDER), size=fs(12, scale),
                   color=BRAND_COLORS["text_muted"]),
           note("서식은 초안을 쓰는 같은 호출에서 함께 만들어져 비용이 거의 늘지 않습니다. 글마다 워크벤치에서 강도를 "
                "바꿀 수 있습니다. 컴플라이언스 검수는 서식 없는 본문 그대로 합니다.")],
        spacing=2,
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
            {"keyword": k, "weight": float(keyword_weights.get(k, 1.0)), "target": k not in non_target}
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
                "정해집니다. 🔑 SEO 키워드 화면에서 이 킷을 골라 재측정하세요.",
                color="#B3261E", size=fs(12, scale),
            ),
            bgcolor="#FDECEA", padding=10, border_radius=8,
        )
    elif freshness["days_left"] is not None:
        freshness_banner = ft.Text(
            f"📈 경쟁도 측정: 가장 오래된 것이 {freshness['oldest_document_age']:.0f}일 전 · "
            f"{freshness['days_left']:.0f}일 후 만료됩니다. 만료되면 전환 가중치가 조용히 꺼지므로, "
            "그 전에 🔑 SEO 키워드 화면에서 재측정하세요.",
            size=fs(12, scale), color=BRAND_COLORS["text_muted"],
        )

    # --- 예시 글 ----------------------------------------------------------------
    few_shot_field = ft.TextField(
        label="예시 글 (여러 개면 빈 줄에 --- 로 구분)",
        value=FEW_SHOT_DELIMITER.join(existing.get("few_shot_samples") or []),
        multiline=True, min_lines=8, max_lines=16, expand=True,
    )

    save_status = ft.Text("", size=fs(12, scale), color="#1B6E3C")

    def on_save(e: ft.Event) -> None:
        core_facts = [line.strip() for line in (core_facts_field.value or "").splitlines() if line.strip()]
        few_shot_samples = [
            s.strip() for s in (few_shot_field.value or "").split(FEW_SHOT_DELIMITER.strip()) if s.strip()
        ]
        new_terminology = {row["term"]: row["desc"] for row in terminology_table.get_rows() if row["term"]}

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
            kit_id,
            sub_brand=sub_brand.value,
            industry=industry.value,
            persona=persona.value,
            tone_and_manner=tone_and_manner.value,
            service_areas=_split(service_areas_field.value),
            product_defaults={k: tf.value.strip() for k, tf in default_fields.items() if (tf.value or "").strip()},
            core_facts=core_facts,
            terminology=new_terminology,
            seo_keywords=new_keywords,
            keyword_weights=new_weights,
            non_target_keywords=new_non_targets,
            default_content_mode=mode_dropdown.value,
            design_template=design_template.value,
            design_strength=design_strength.value,
            few_shot_samples=few_shot_samples,
        )
        fact_banner.content.value = fact_freshness.summary(repo.get_brand_kit(kit_id))
        fact_banner.visible = bool(fact_banner.content.value)
        save_status.value = (
            f"✅ '{kit_name}' 킷을 저장했습니다. (핵심 팩트 {len(core_facts)} · 용어 {len(new_terminology)} · "
            f"SEO 키워드 {len(new_keywords)} · 예시 글 {len(few_shot_samples)})"
        )
        page.update()

    save_button = ft.FilledButton(f"'{kit_name}' 킷 저장", icon=ft.Icons.SAVE, on_click=on_save)

    # --- 회사 공통 -------------------------------------------------------------
    brand_name = ft.TextField(label="기업명", value=existing.get("brand_name") or "", expand=True)
    homepage = ft.TextField(label="홈페이지", value=existing.get("homepage") or "", expand=True)
    naver_blog_id = ft.TextField(
        label="네이버 블로그 아이디", value=existing.get("naver_blog_id") or "",
        helper="blog.naver.com/<아이디>. 반자동 게시가 이 블로그로 글을 올립니다.", expand=True,
    )
    instagram_handle = ft.TextField(label="인스타그램 핸들", value=existing.get("instagram_handle") or "", expand=True)
    guardrail_enabled = ft.Switch(
        label="🛡️ 표시·광고 컴플라이언스 가드레일", value=bool(existing.get("guardrail_enabled", True)),
    )
    blacklist_table = EditableTable(
        columns=[ColumnSpec("bad", "금기어", "text"), ColumnSpec("good", "치환어", "text")],
        rows=[{"bad": k, "good": v} for k, v in (existing.get("blacklist_map") or {}).items()],
    )
    news_exclude_field = ft.TextField(
        label="뉴스 큐레이션 제외어 (쉼표로 구분)",
        value=", ".join(existing.get("news_exclude_terms") or []),
        helper="기사 제목·요약에 이 말이 있으면 뉴스 검색 결과에서 뺍니다 (띄어쓰기 무시).",
        expand=True,
    )
    active_channels = set(enabled_channels(existing))
    channel_checks = {
        key: ft.Checkbox(label=label, value=key in active_channels) for key, label in SNS_CHANNELS.items()
    }
    format_mode = (repo.get_app_state(formatting.NAVER_FORMAT_STATE_KEY) or {}).get("value") \
        or formatting.DEFAULT_NAVER_FORMAT_MODE
    format_mode_group = ft.RadioGroup(value=format_mode, content=ft.Column([
        ft.Radio(value="editor", label="에디터 서식 우선 — 인용구·구분선·요약 박스를 HTML 서식으로 붙여 넣습니다"),
        ft.Radio(value="symbol", label="기호로 대체 — 인용구는 ❝ ❞, 구분선은 ────, 요약 박스는 📌 제목 + 선으로 넣습니다"),
    ], spacing=2))

    guardrail_warning_box = ft.Container(
        content=ft.Text(
            "가드레일이 꺼져 있습니다. 결과 보장·요금 오표시·인증 확대 같은 표현이 검수 없이 발행될 수 있습니다.",
            color="#B3261E", size=fs(12, scale),
        ),
        bgcolor="#FDECEA", padding=10, border_radius=8,
        visible=not bool(existing.get("guardrail_enabled", True)),
    )
    common_status = ft.Text("", size=fs(12, scale), color="#1B6E3C")

    def on_save_common(e: ft.Event) -> None:
        new_blacklist = {row["bad"]: row["good"] for row in blacklist_table.get_rows() if row["bad"]}
        repo.save_company_profile(
            brand_name=brand_name.value,
            homepage=homepage.value,
            naver_blog_id=naver_blog_id.value,
            instagram_handle=instagram_handle.value,
            guardrail_enabled=guardrail_enabled.value,
            blacklist_map=new_blacklist,
            news_exclude_terms=_split(news_exclude_field.value),
        )
        repo.save_app_settings(enabled_channels=[k for k, cb in channel_checks.items() if cb.value])
        repo.set_app_state(formatting.NAVER_FORMAT_STATE_KEY, {"value": format_mode_group.value})
        guardrail_warning_box.visible = not guardrail_enabled.value
        common_status.value = f"✅ 회사 공통 값을 저장했습니다. (금기어 {len(new_blacklist)}) 모든 킷에 적용됩니다."
        page.update()

    common_save_button = ft.FilledButton("회사 공통 저장", icon=ft.Icons.SAVE, on_click=on_save_common)

    # --- 제목 반복 방지 --------------------------------------------------------
    history_count = repo.title_history_count()
    history_list = ft.Column(
        [ft.Text(f"• {t}", size=fs(12, scale)) for t in repo.recent_titles(50)],
        scroll=ft.ScrollMode.AUTO, height=200, visible=False,
    )

    def toggle_history(e: ft.Event) -> None:
        history_list.visible = not history_list.visible
        page.update()

    def clear_history(e: ft.Event) -> None:
        repo.clear_title_history()
        history_list.controls = []
        common_status.value = "제목 이력을 삭제했습니다."
        page.update()

    history_section = ft.Column([
        ft.Text("🎲 제목 반복 방지", weight=ft.FontWeight.BOLD),
        ft.Text(
            f"지금까지 생성한 제목 {history_count}건을 기억해, 새 제목이 과거 제목과 문장 구조까지 "
            "겹치면 자동으로 다시 짓습니다. 같은 블로그에 올리므로 킷과 관계없이 함께 봅니다. "
            "이 이력은 캠페인을 삭제해도 남습니다.",
            size=fs(12, scale), color=BRAND_COLORS["text_muted"],
        ),
        ft.Row([
            ft.TextButton(f"이력 {history_count}건 보기/숨기기", on_click=toggle_history),
            ft.TextButton("🗑️ 제목 이력 전체 삭제", on_click=clear_history),
        ]),
        history_list,
    ])

    return ft.Column(
        [
            ft.Text("브랜드 킷", size=fs(24, scale), weight=ft.FontWeight.BOLD),
            note("여기 등록한 내용은 매 생성마다 프롬프트에 그대로 주입됩니다 (유사도 검색이 아니라 전체 주입). "
                 "킷 값과 회사 공통 값은 저장 버튼이 따로 있습니다."),
            guardrail_warning_box,
            _build_kit_list(page, state, render, scale, kits, archived, kit_id),

            section(f"✏️ '{kit_name}' 킷 편집",
                    "이 킷으로 쓰는 글에만 쓰입니다. 저장하지 않은 수정은 다른 킷을 편집하러 가면 사라집니다.",
                    BRAND_COLORS["primary"]),
            sub_brand,
            industry,
            persona,
            tone_and_manner,
            ft.Text("📍 서비스 지역", weight=ft.FontWeight.BOLD),
            service_areas_field,
            ft.Text("🧾 서비스·이용 정보 기본값", weight=ft.FontWeight.BOLD),
            note("이 킷의 글 유형과 워크벤치 [📥 브랜드 킷 기본값 채우기]가 이 값을 씁니다. 채운 값은 그 글에 "
                 "'반드시 들어갈 사실'로 전달되므로 확인된 내용만 적으세요."),
            *default_rows,
            ft.Text("🏭 핵심 팩트", weight=ft.FontWeight.BOLD),
            fact_banner,
            core_facts_field,
            ft.Text("📖 용어집", weight=ft.FontWeight.BOLD),
            terminology_table.build(),
            ft.Text("🔍 SEO 키워드 (네이버 블로그 전용)", weight=ft.FontWeight.BOLD),
            note("이 킷의 사업 키워드만 넣어주세요. 키워드를 새로 고르거나 동네 키워드를 더하는 작업은 🔑 SEO 키워드 "
                 "화면에서 이 킷을 고른 뒤 합니다. 🎯 '검색 타깃'을 끈 키워드는 본문에는 써도 제목 키워드로는 고르지 않습니다."),
            keywords_table.build(),
            *([freshness_banner] if freshness_banner else []),
            mode_dropdown,
            mode_captions,
            ft.Text("🎨 원고 서식", weight=ft.FontWeight.BOLD),
            ft.Row([design_template, design_strength], spacing=10, wrap=True),
            design_captions,
            ft.Text("✍️ 예시 글", weight=ft.FontWeight.BOLD),
            note("회사가 실제로 쓴 글이 생기면 넣으세요. 지어낸 예시는 말투뿐 아니라 내용까지 따라 하게 만듭니다."),
            few_shot_field,
            ft.Row([save_button, save_status], wrap=True),

            section("🏢 회사 공통 — 모든 킷에 적용",
                    "사회적협동조합 강서나눔돌봄센터의 계정·검수 기준·채널입니다.", BRAND_COLORS["primary_dark"]),
            ft.Text("🎨 브랜드 컬러", weight=ft.FontWeight.BOLD),
            palette_row(scale=scale),
            ft.Row([brand_name]),
            ft.Row([homepage, naver_blog_id, instagram_handle]),
            guardrail_enabled,
            ft.Text("🚫 금기어 치환 사전 (과장·오인 광고 방지)", weight=ft.FontWeight.BOLD),
            blacklist_table.build(),
            ft.Text("📰 뉴스 큐레이션 제외어", weight=ft.FontWeight.BOLD),
            news_exclude_field,
            ft.Text("📣 함께 만들 채널", weight=ft.FontWeight.BOLD),
            note("네이버 블로그 본문과 발행 태그는 항상 만듭니다. 운영하지 않는 채널을 끄면 생성이 빨라지고 "
                 "그 채널의 AI 호출(작성 + 검수)이 0이 됩니다."),
            ft.Row(list(channel_checks.values()), wrap=True),
            ft.Text("🎨 네이버 서식 붙여넣기", weight=ft.FontWeight.BOLD),
            note("굵게·형광·소제목·목록은 어느 쪽이든 서식으로 붙여 넣습니다. 스마트에디터가 인용구·구분선·표를 "
                 "제대로 바꾸지 못하면 '기호로 대체'를 고르세요. 인용구·구분선 모양은 에디터에서 한 번 눌러 바꿉니다."),
            format_mode_group,
            ft.Row([common_save_button, common_status], wrap=True),
            ft.Divider(),
            history_section,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10,
    )
