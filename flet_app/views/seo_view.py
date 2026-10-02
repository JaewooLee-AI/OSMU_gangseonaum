"""🔑 SEO 키워드 — 어떤 검색어로 노출을 노릴지 정하는 화면.

키워드 고르기·분야 추가·수치 유지는 원래 ⚙️ 설정 → 네이버 API 탭 맨 아래에 있었습니다.
API 키를 넣는 '설정'과 무엇을 노릴지 정하는 '전략'이 한 탭에 섞여 있어, 담당자가
키워드를 손보려면 키 입력 화면을 지나 내려가야 했습니다. 키는 설정에 남기고, 전략은
여기로 옮겼습니다. 각 섹션의 동작은 그대로입니다 (settings_view의 같은 함수를 씁니다).

새로 더한 것은 📍 동네 키워드 찾기 하나입니다 — 블로그 이력이 거의 없는 지금은
'가사도우미' 같은 큰 검색어를 이길 수 없고, 이길 수 있는 것은 동네 단위 검색어입니다.
"""
from __future__ import annotations

import flet as ft

from ai_workers import keyword_curator, keyword_research
from core import repo

from flet_app.state import AppState
from flet_app.theme import BRAND_COLORS, fs
from flet_app.views.settings_view import (
    _build_keyword_diagnostic_section,
    _build_sweep_wizard,
    _warn_box,
)


# [➕ 사업 분야 추가]는 검색량이 작은 부수 사업이 [새로 고르기]에서 주력 상품에 밀려 빠지는 회사를
# 위한 기능입니다(원본 더스티치의 교육 분야). 이 회사는 반대로 SNS 대상 사업(주간보호·방문요양)이
# 검색량이 가장 크고 부수 사업(가사)은 SNS가 필요 없어서, [새로 고르기]와 📍 동네 키워드 찾기로
# 충분합니다. 화면을 줄이려고 숨깁니다 — 다른 회사에 쓰려면 True로 바꾸면 됩니다.
SHOW_CATEGORY_ADDER = False


def _build_local_finder(page: ft.Page, scale: float, rebuild) -> ft.Control:
    kit = repo.get_brand_kit()
    pool = kit.get("seo_keywords") or []
    areas = kit.get("service_areas") or []
    keys_ok = bool(repo.get_searchad_settings())
    state = repo.get_app_state("local_sweep") or {}

    areas_field = ft.TextField(
        label="동네 (쉼표로 구분)", value=", ".join(state.get("areas") or areas), expand=True,
        helper="🧵 브랜드 킷의 서비스 지역에서 가져왔습니다. 여기서 바꾸면 이번 조회에만 쓰입니다.",
    )
    services_field = ft.TextField(
        label="서비스어 (쉼표로 구분)",
        value=", ".join(state.get("services") or keyword_research.DEFAULT_LOCAL_SERVICE_TERMS),
        expand=True,
        helper="동네 이름 뒤에 붙여 검색하는 말. 제공하지 않는 서비스(입주청소 등)는 넣지 마세요.",
    )
    status = ft.Text("", size=fs(12, scale), color="#B3261E")

    def _split(text: str) -> list[str]:
        return [t.strip() for t in (text or "").split(",") if t.strip()]

    def on_measure(e: ft.Event) -> None:
        area_list, service_list = _split(areas_field.value), _split(services_field.value)
        if not area_list or not service_list:
            status.value = "동네와 서비스어를 하나 이상 적어주세요."
            status.update()
            return
        measure_button.disabled = True
        measure_button.update()
        status.value = f"⏳ 조합 {len(area_list) * len(service_list)}개의 검색량을 재는 중… (무료)"
        status.color = BRAND_COLORS["text_muted"]
        status.update()

        def _work() -> None:
            try:
                rows = keyword_research.measure_local(area_list, service_list)
            except Exception as exc:  # noqa: BLE001
                status.value = f"❌ {exc}"
                status.color = "#B3261E"
                measure_button.disabled = False
                status.update()
                measure_button.update()
                return
            repo.set_app_state("local_sweep", {"areas": area_list, "services": service_list, "rows": rows})
            rebuild()

        page.run_thread(_work)

    measure_button = ft.FilledButton("📏 동네 키워드 검색량 재기 (무료)", on_click=on_measure, disabled=not keys_ok)

    controls: list[ft.Control] = [
        ft.Text("📍 동네 키워드 찾기", weight=ft.FontWeight.BOLD, size=fs(16, scale)),
        ft.Text(
            "블로그 글이 아직 적어 네이버의 블로그 신뢰 점수(C-Rank)가 낮을 때는 '가사도우미'처럼 "
            "글이 수십만 개 쌓인 검색어에서 상위에 오르기 어렵습니다. '화곡동 가사도우미'처럼 동네 "
            "이름이 붙은 검색어는 검색량이 작아도 경쟁 글이 적고, 검색하는 사람이 곧 서비스 지역의 "
            "고객입니다. 동네 × 서비스어 조합의 실제 검색량을 재고, 고른 것만 SEO 키워드에 더합니다.",
            size=fs(12, scale), color=BRAND_COLORS["text_muted"],
        ),
    ]
    controls += [areas_field, services_field, ft.Row([measure_button]), status]

    rows = state.get("rows")
    if rows is not None:
        if not rows:
            controls.append(_warn_box(
                f"월 {keyword_research.LOCAL_MIN_VOLUME}회 이상 검색되는 조합이 없습니다. 서비스어를 "
                "바꿔 보거나(예: 청소도우미 → 가사도우미) 동네 이름 표기를 바꿔 보세요(예: 마곡 → 마곡동).",
                scale,
            ))
        else:
            checks: list[tuple[str, ft.Checkbox]] = []
            controls.append(ft.Text(
                f"월 {keyword_research.LOCAL_MIN_VOLUME}회 이상 검색되는 조합 {len(rows)}개 — 실제로 글을 쓸 "
                "동네만 고르세요. 고른 키워드는 '구매 직결'(전환 가중치 2.0)로 더해지고, 경쟁도는 고른 "
                "것만 잽니다(키워드당 유료 호출 1회).",
                size=fs(12, scale), color="#1B6E3C",
            ))
            for row in rows:
                in_pool = row["keyword"] in pool
                docs = row.get("documents")
                docs_text = f" · 블로그 글 {docs:,}개" if docs is not None else ""
                cb = ft.Checkbox(
                    label=f"{row['keyword']} — 월 {row['estimated_volume']:,}회{docs_text}"
                    + (" (이미 SEO 키워드에 있음)" if in_pool else ""),
                    value=False, disabled=in_pool,
                )
                if not in_pool:
                    checks.append((row["keyword"], cb))
                controls.append(cb)

            apply_status = ft.Text("", size=fs(12, scale))

            def on_apply(e: ft.Event) -> None:
                chosen = [kw for kw, cb in checks if cb.value]
                if not chosen:
                    apply_status.value = "추가할 키워드를 체크하세요."
                    apply_status.update()
                    return
                apply_button.disabled = True
                apply_button.update()
                apply_status.value = f"⏳ {len(chosen)}개를 더하고 경쟁도를 재는 중…"
                apply_status.update()

                def _work() -> None:
                    try:
                        proposal = {"groups": {"purchase": [{"keyword": kw} for kw in chosen]}}
                        applied = keyword_curator.apply_and_measure(pool + chosen, proposal)
                    except Exception as exc:  # noqa: BLE001
                        apply_status.value = f"❌ {exc}"
                        apply_status.color = "#B3261E"
                        apply_button.disabled = False
                        apply_status.update()
                        apply_button.update()
                        return
                    repo.clear_app_state("local_sweep")
                    repo.set_app_state("local_sweep_done", {"text": (
                        f"✅ 동네 키워드 {len(chosen)}개({', '.join(chosen)})를 더했습니다 — SEO 키워드 총 "
                        f"{applied['pool']}개 (유료 호출 {applied['calls']}회)."
                    )})
                    rebuild()

                page.run_thread(_work)

            def on_discard(e: ft.Event) -> None:
                repo.clear_app_state("local_sweep")
                rebuild()

            apply_button = ft.FilledButton("✅ 고른 동네 키워드 추가", on_click=on_apply)
            controls += [ft.Row([apply_button, ft.OutlinedButton("버리기", on_click=on_discard)]), apply_status]

    done = (repo.get_app_state("local_sweep_done") or {}).get("text")
    if done and rows is None:
        controls.append(ft.Text(done, size=fs(12, scale), color="#1B6E3C"))
    return ft.Column(controls, spacing=8)


def build(page: ft.Page, state: AppState) -> ft.Control:
    scale = state.font_scale
    local_box = ft.Container()
    wizard_box = ft.Container()

    def rebuild() -> None:
        local_box.content = _build_local_finder(page, scale, rebuild)
        wizard_box.content = _build_sweep_wizard(page, scale, rebuild, SHOW_CATEGORY_ADDER)
        local_box.update()
        wizard_box.update()

    local_box.content = _build_local_finder(page, scale, rebuild)
    wizard_box.content = _build_sweep_wizard(page, scale, rebuild, SHOW_CATEGORY_ADDER)

    keys_missing = not (repo.get_naver_api_settings() and repo.get_searchad_settings())
    return ft.Column(
        [
            ft.Text("SEO 키워드", size=fs(24, scale), weight=ft.FontWeight.BOLD),
            ft.Text(
                "네이버 블로그 글이 어떤 검색어로 노출될지 정합니다. 여기서 정한 키워드는 🧵 브랜드 킷의 "
                "SEO 키워드 표에 들어가고, 글마다 주제에 맞는 것만 골라 씁니다.",
                size=fs(12, scale), color=BRAND_COLORS["text_muted"],
            ),
            *([_warn_box(
                "네이버 API 키가 아직 없습니다. ⚙️ 설정 → 🔍 네이버 API에서 API HUB와 검색광고 키를 "
                "등록하면 아래 기능이 켜집니다.", scale,
            )] if keys_missing else []),
            ft.Divider(),
            local_box,
            ft.Divider(),
            wizard_box,
            ft.Divider(),
            _build_keyword_diagnostic_section(page, scale),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
