"""당근 비즈프로필 '소식' 미리보기 — Flet 네이티브.

A neighbour's-notice card: profile line, title, body, and the first photos
of the post. The point of the preview is the same as for the other channels —
see how long the body reads on a phone-width card before pasting it.
"""
from __future__ import annotations

import flet as ft

from core import storage
from flet_app.simulators.base import all_images

CARD_WIDTH = 390
DAANGN_ORANGE = "#FF6F0F"
MAX_PREVIEW_PHOTOS = 3


def render(campaign: dict, profile_name: str = "비즈프로필", area: str = "") -> ft.Control:
    post = campaign.get("daangn_post") or {}
    title = (post.get("title") or "").strip()
    body = (post.get("body") or "").strip()
    if not title and not body:
        return ft.Container(
            width=CARD_WIDTH, height=200, alignment=ft.Alignment.CENTER,
            border=ft.Border.all(1, "#EEEEEE"), border_radius=12,
            content=ft.Text("당근 소식이 아직 생성되지 않았습니다.", color="#868B94", size=14),
        )

    images = all_images(campaign.get("content") or "", campaign.get("storage_file_paths") or [])
    photos = [
        ft.Container(
            content=ft.Image(src=str(storage.abs_path(path)), width=110, height=110, fit=ft.BoxFit.COVER),
            border_radius=8, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )
        for path in images[:MAX_PREVIEW_PHOTOS]
    ]

    header = ft.Row(
        [
            ft.Container(
                content=ft.Text("🥕", size=18), width=36, height=36, border_radius=18,
                bgcolor="#FFF1E8", alignment=ft.Alignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Text(profile_name, size=14, weight=ft.FontWeight.BOLD, color="#212124"),
                    ft.Text(f"{area} · 소식" if area else "소식", size=12, color="#868B94"),
                ],
                spacing=0,
            ),
        ],
        spacing=10,
    )

    return ft.Container(
        width=CARD_WIDTH,
        padding=16,
        border=ft.Border.all(1, "#EEEEEE"),
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            [
                header,
                ft.Text(title or "(제목 없음)", size=17, weight=ft.FontWeight.BOLD, color="#212124"),
                *([ft.Row(photos, spacing=6)] if photos else []),
                ft.Text(body, size=15, color="#212124", selectable=True),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text("문의하기", color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                            bgcolor=DAANGN_ORANGE, border_radius=6,
                            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                        ),
                        ft.Text(f"제목 {len(title)}자 · 본문 {len(body)}자", size=11, color="#868B94"),
                    ],
                    spacing=12,
                ),
            ],
            spacing=10,
        ),
    )
