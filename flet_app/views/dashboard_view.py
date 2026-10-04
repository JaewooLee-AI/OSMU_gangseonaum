"""파이프라인 대시보드.

원본의 `core/theme.py` HTML(`stat_card`/`status_chip`)이 아니라, 브랜드 킷
화면부터 써온 `flet_app/theme.py`의 네이티브 버전을 그대로 재사용한다.
"""
from __future__ import annotations

import flet as ft

from ai_workers import content_mode, fact_freshness, post_types, topic_calendar
from core import repo, storage

from flet_app.components.collapsible import collapsible
from flet_app.state import AppState
from flet_app.theme import BRAND_COLORS, fs, stat_card, status_chip

BOARD_COLUMNS = [
    ("awaiting_media", "소재 대기"),
    ("processing", "생성 중"),
    ("draft", "초안 완료"),
    ("ready_to_publish", "게시 대기"),
    ("published", "게시 완료"),
]


def _job_card(job: dict, scale: float) -> ft.Control:
    icon = "📰" if job.get("source_type") == "news" else "✍️"
    title = job.get("title") or job.get("source_url") or job["id"][:8]
    photos = len(job.get("storage_file_paths") or [])
    return ft.Container(
        content=ft.Column([
            ft.Text(f"{icon} {title}", size=fs(12, scale), weight=ft.FontWeight.BOLD, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Text(f"{job.get('created_at', '')} · 사진 {photos}장", size=fs(10, scale), color=BRAND_COLORS["text_muted"]),
            status_chip(job["status"], scale),
        ], spacing=4),
        bgcolor=ft.Colors.WHITE, border_radius=8, padding=10, border=ft.Border.all(1, "#14000000"),
    )


def _build_board(campaigns: list[dict], scale: float) -> ft.Control:
    columns: list[ft.Control] = []
    for status_key, column_title in BOARD_COLUMNS:
        jobs = [c for c in campaigns if c["status"] == status_key][:12]
        col_children: list[ft.Control] = [
            ft.Text(f"{column_title} ({len([c for c in campaigns if c['status'] == status_key])})",
                    size=fs(13, scale), weight=ft.FontWeight.BOLD),
        ]
        if not jobs:
            col_children.append(ft.Text("항목 없음", size=fs(11, scale), color=BRAND_COLORS["text_muted"]))
        col_children += [_job_card(j, scale) for j in jobs]
        columns.append(ft.Container(content=ft.Column(col_children, spacing=8), expand=True))
    return ft.Row(columns, spacing=12, vertical_alignment=ft.CrossAxisAlignment.START)


def _build_failed_section(campaigns: list[dict], scale: float, refresh) -> list[ft.Control]:
    failed = [c for c in campaigns if c["status"] == "failed"]
    if not failed:
        return []

    out: list[ft.Control] = [ft.Divider(), ft.Text("⚠️ 실패한 작업", size=fs(16, scale), weight=ft.FontWeight.BOLD)]
    for job in failed:
        job_id = job["id"]

        def on_retry(e: ft.Event, job_id: str = job_id) -> None:
            repo.update_campaign(job_id, status="awaiting_media", publish_error=None)
            refresh(True)

        def on_delete(e: ft.Event, job_id: str = job_id) -> None:
            repo.delete_campaign(job_id)
            refresh(True)

        out.append(ft.Container(
            content=ft.Column([
                ft.Text(job.get("title") or job.get("source_url") or job["id"][:8], weight=ft.FontWeight.BOLD, size=fs(13, scale)),
                ft.Text(job.get("publish_error") or "원인 미기록", size=fs(11, scale), color=BRAND_COLORS["text_muted"]),
                ft.Row([
                    ft.OutlinedButton("🔁 다시 시도", on_click=on_retry),
                    ft.OutlinedButton("🗑️ 삭제", on_click=on_delete),
                ], spacing=8),
            ], spacing=6),
            border=ft.Border.all(1, "#E4DCC8"), border_radius=10, padding=12,
        ))
    return out


def _build_reset_section(page: ft.Page, scale: float, campaigns: list[dict], file_count: int, total_bytes: int, refresh) -> list[ft.Control]:
    confirm = {"value": False}
    action_box = ft.Container()

    def build_actions() -> ft.Control:
        if not confirm["value"]:
            def on_ask(e: ft.Event) -> None:
                confirm["value"] = True
                action_box.content = build_actions()
                action_box.update()

            return ft.FilledButton("🗑️ 콘텐츠 초기화", on_click=on_ask)

        def on_confirm(e: ft.Event) -> None:
            removed = repo.reset_generated_content()
            files_removed = storage.clear_all()
            confirm["value"] = False
            refresh(True)
            page.show_dialog(ft.SnackBar(ft.Text(
                f"초기화했습니다 — 캠페인 {removed['campaigns']}건, 사진 {files_removed}장, "
                f"제목 이력 {removed['titles']}건 삭제됨."
            )))

        def on_cancel(e: ft.Event) -> None:
            confirm["value"] = False
            action_box.content = build_actions()
            action_box.update()

        return ft.Column([
            ft.Container(
                content=ft.Text(
                    "정말 삭제할까요? 되돌릴 수 없습니다. 위에 적힌 캠페인·사진·제목 이력이 전부 사라집니다.",
                    size=fs(12, scale), color="#8A6D3B",
                ),
                bgcolor="#FFF6E5", padding=10, border_radius=8,
            ),
            ft.Row([
                ft.FilledButton("네, 초기화합니다", on_click=on_confirm),
                ft.OutlinedButton("취소", on_click=on_cancel),
            ], spacing=8),
        ], spacing=8)

    action_box.content = build_actions()

    body = ft.Column([
        ft.Text(
            "워크벤치·뉴스 큐레이션·네이버 게시로 만들어진 것만 지웁니다 — 캠페인(초안·인스타/X/쇼츠·"
            "컴플라이언스 리포트), 업로드한 사진, 제목 반복 방지 이력. 브랜드 킷, API 키, LLM 설정, "
            "키워드·이미지 분석 캐시는 그대로 남습니다.",
            size=fs(11, scale), color=BRAND_COLORS["text_muted"],
        ),
        ft.Text(
            f"- 캠페인 {len(campaigns)}건\n"
            f"- 업로드 사진 {file_count}장 ({total_bytes / 1_048_576:.1f}MB)\n"
            f"- 제목 이력 {repo.title_history_count()}건",
            size=fs(11, scale),
        ),
        action_box,
    ], spacing=8)

    return [ft.Divider()] + collapsible("⚠️ 콘텐츠 초기화", body)


# 게시 주기 목표 — 블로그가 한 주제를 '꾸준히' 다루는지가 네이버 C-Rank의 핵심이라,
# 글 한 편의 완성도보다 이 숫자가 먼저입니다. 화면에서 바꿀 수 있습니다.
WEEKLY_TARGET_STATE_KEY = "weekly_post_target"
DEFAULT_WEEKLY_TARGET = 2


def _build_cadence(scale: float, refresh) -> list[ft.Control]:
    stats = repo.publish_stats()
    target = int((repo.get_app_state(WEEKLY_TARGET_STATE_KEY) or {}).get("value") or DEFAULT_WEEKLY_TARGET)
    days = stats["days_since"]
    if stats["total"] == 0:
        verdict, kind = "아직 게시한 글이 없습니다. 아래 추천 주제 하나로 시작해 보세요.", "warning"
    elif stats["last7"] >= target:
        verdict, kind = f"이번 주 목표({target}편)를 채웠습니다.", "success"
    elif days is not None and days > 7:
        verdict, kind = (
            f"마지막 게시 후 {days:.0f}일이 지났습니다. 네이버는 꾸준히 쓰는 블로그를 더 신뢰합니다 — "
            "이번 주에 한 편을 올려 보세요."
        ), "warning"
    else:
        verdict, kind = f"이번 주 {stats['last7']}/{target}편 — {target - stats['last7']}편 남았습니다.", "info"
    colors = {"success": ("#1B6E3C", "#E8F5E9"), "warning": ("#8A6D3B", "#FFF6E5"), "info": ("#2F6B7A", "#E7F1F3")}

    target_field = ft.Dropdown(
        label="주간 목표", value=str(target), width=130,
        options=[ft.DropdownOption(key=str(n), text=f"주 {n}편") for n in (1, 2, 3, 4, 5)],
    )

    def on_target(e: ft.Event) -> None:
        repo.set_app_state(WEEKLY_TARGET_STATE_KEY, {"value": int(target_field.value)})
        refresh(True)

    target_field.on_select = on_target
    color, bg = colors[kind]
    return [
        ft.Text("📈 게시 주기", size=fs(16, scale), weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.Container(content=stat_card("최근 7일", f"{stats['last7']}편", f"목표 주 {target}편", scale), expand=True),
            ft.Container(content=stat_card("최근 30일", f"{stats['last30']}편", f"누적 {stats['total']}편", scale), expand=True),
            ft.Container(content=stat_card(
                "마지막 게시", f"{days:.0f}일 전" if days is not None else "—", "네이버 게시 완료 기준", scale,
            ), expand=True),
            target_field,
        ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Container(content=ft.Text(verdict, size=fs(12, scale), color=color), bgcolor=bg, padding=10, border_radius=8),
    ]


def _start_topic(state, topic: dict) -> None:
    """추천 주제로 새 글을 만들고 워크벤치로 갑니다 — 글 유형의 모드·서비스 정보도 함께."""
    brand_kit = repo.get_brand_kit()
    spec = post_types.get(topic.get("post_type")) or {}
    mode = spec.get("mode") or content_mode.resolve(None, brand_kit)["key"]
    created = repo.insert_campaign(
        source_type="manual",
        status="awaiting_media",
        memo=f"{repo.TOPIC_MEMO_PREFIX}{topic['title']}\n{topic['memo']}",
        post_type=topic.get("post_type"),
        content_mode=mode,
        product_fields=post_types.default_product_fields(topic.get("post_type"), brand_kit, {}),
    )
    repo.link_topic(created["id"], topic["title"])
    state.pending_workbench_campaign_id = created["id"]
    if state.navigate_to_workbench:
        state.navigate_to_workbench()


def _build_topics(scale: float, state) -> list[ft.Control]:
    used = repo.used_topic_titles()
    picks = topic_calendar.suggestions(used=used)

    def row(topic: dict) -> ft.Control:
        spec = post_types.get(topic.get("post_type")) or {}
        done = topic["title"] in used
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(("✅ " if done else "") + topic["title"], size=fs(13, scale), weight=ft.FontWeight.BOLD),
                    ft.Text(spec.get("label", ""), size=fs(11, scale), color=BRAND_COLORS["text_muted"]),
                ], spacing=2, expand=True),
                ft.OutlinedButton(
                    "다시 쓰기" if done else "✍️ 이 주제로 새 글",
                    on_click=lambda e, t=topic: _start_topic(state, t),
                ),
            ]),
            bgcolor=ft.Colors.WHITE, border_radius=8, padding=10, border=ft.Border.all(1, "#14000000"),
        )

    out: list[ft.Control] = [
        ft.Text("📅 이번 달 추천 주제", size=fs(16, scale), weight=ft.FontWeight.BOLD),
        ft.Text(
            "누르면 메모가 채워진 새 글이 워크벤치에 열립니다. 메모의 [ ] 자리에 현장 이야기를 한 줄이라도 "
            "넣으면 다른 글과 겹치지 않는 글이 나옵니다.",
            size=fs(11, scale), color=BRAND_COLORS["text_muted"],
        ),
    ]
    out += [row(t) for t in picks["this_month"]]
    if picks["next_month"]:
        out.append(ft.Text(
            f"{picks['next']}월 미리 준비 — 계절 글은 2~3주 먼저 올려야 검색될 때 이미 자리를 잡고 있습니다.",
            size=fs(11, scale), color=BRAND_COLORS["text_muted"],
        ))
        out += [row(t) for t in picks["next_month"]]
    if picks["evergreen"]:
        out.append(ft.Text("상시 주제", size=fs(12, scale), weight=ft.FontWeight.BOLD))
        out += [row(t) for t in picks["evergreen"]]
    return out


def _build_body(page: ft.Page, scale: float, refresh, state=None) -> ft.Control:
    campaigns = repo.list_campaigns()
    counts = repo.campaign_status_counts()
    usage = repo.usage_totals()
    file_count, total_bytes = storage.storage_usage()

    active = counts.get("awaiting_media", 0) + counts.get("queued", 0) + counts.get("processing", 0)
    drafts = counts.get("draft", 0)
    published = counts.get("published", 0)
    saved = usage["saved_tokens"]
    spent = usage["input_tokens"] + usage["output_tokens"]
    ratio = f"절감률 {saved / (saved + spent) * 100:.0f}%" if (saved + spent) else "아직 호출 없음"

    def on_refresh(e: ft.Event) -> None:
        refresh(True)

    controls: list[ft.Control] = [
        ft.Text("파이프라인 대시보드", size=fs(24, scale), weight=ft.FontWeight.BOLD),
        ft.Text(
            "소재 수집 → 초안 생성 → 게시까지의 진행 상황과, 이번까지 절약된 토큰을 한눈에 봅니다.",
            size=fs(12, scale), color=BRAND_COLORS["text_muted"],
        ),
        ft.Row([
            ft.Container(content=stat_card("작업 중", str(active), "소재 대기 + 생성 중", scale), expand=True),
            ft.Container(content=stat_card("초안 완료", str(drafts), "검수 후 게시 가능", scale), expand=True),
            ft.Container(content=stat_card("게시 완료", str(published), f"사진 {file_count}장 · {total_bytes / 1_048_576:.1f}MB", scale), expand=True),
            ft.Container(content=stat_card("절약된 토큰", f"{saved:,}", ratio, scale), expand=True),
        ], spacing=12),
    ]
    freshness_note = fact_freshness.summary(repo.get_brand_kit())
    if freshness_note:
        controls.append(ft.Container(
            content=ft.Text(freshness_note, size=fs(12, scale), color="#8A6D3B"),
            bgcolor="#FFF6E5", padding=10, border_radius=8,
        ))
    controls += _build_cadence(scale, refresh)
    if state is not None:
        controls += _build_topics(scale, state)
    controls += [
        ft.Divider(),
        ft.Text("🗂️ 진행 상황", size=fs(16, scale), weight=ft.FontWeight.BOLD),
        _build_board(campaigns, scale),
    ]
    controls += _build_failed_section(campaigns, scale, refresh)
    controls += [ft.Divider(), ft.OutlinedButton("🔄 새로고침", on_click=on_refresh)]
    controls += _build_reset_section(page, scale, campaigns, file_count, total_bytes, refresh)

    return ft.Column(controls, spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)


def build(page: ft.Page, state: AppState) -> ft.Control:
    scale = state.font_scale
    root = ft.Container(expand=True)

    def refresh(live: bool) -> None:
        root.content = _build_body(page, scale, refresh, state)
        if live:
            root.update()

    refresh(False)
    return root
