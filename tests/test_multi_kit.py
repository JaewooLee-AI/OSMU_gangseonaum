"""브랜드 킷 두 개(돌봄센터 · 가사서비스) — 새 설치 시드, 예전 한 킷 설치의 자동 분리, 킷 관리.

예전 설치는 brand_kit 한 줄(id = 1)에 기본 화자(돌봄센터)와 보조 화자(house_voice = 가사서비스)가
함께 있었습니다. 고객 PC의 데이터가 그 구조이므로, 그 모양의 DB를 만들어 첫 실행을 흉내 냅니다.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from ai_workers import post_types
from core import brand_seed as B
from core import db, repo

# 예전(한 킷) 구조의 brand_kit — main 브랜치 core/db.py와 같은 컬럼.
_OLD_BRAND_KIT_DDL = """
create table brand_kit (
    id integer primary key check (id = 1),
    brand_name text, sub_brand text, industry text, homepage text, persona text, tone_and_manner text,
    guardrail_enabled integer not null default 1, naver_blog_id text, instagram_handle text,
    core_facts text not null default '[]', few_shot_samples text not null default '[]',
    terminology text not null default '{}', seo_keywords text not null default '[]',
    keyword_weights text not null default '{}', non_target_keywords text not null default '[]',
    default_content_mode text not null default 'balanced', service_areas text not null default '[]',
    product_defaults text not null default '{}', care_defaults text not null default '{}',
    house_voice text not null default '{}', news_exclude_terms text not null default '[]',
    enabled_channels text not null default '["instagram", "x", "shorts", "daangn"]',
    blacklist_map text not null default '{}', default_generation_vendor text, vision_vendor text,
    vision_quality text not null default 'economy', vision_enabled integer not null default 1,
    updated_at text not null default (datetime('now'))
);
"""

# 담당자가 키워드 작업으로 더한 동네 키워드 — 나눌 때 버리지 않아야 합니다.
_USER_CARE_KW = "화곡동 주간보호센터"
_USER_HOUSE_KW = "화곡동 가사도우미"
_USER_FACT = "2026년 11월부터 토요일 오후 상담을 받습니다."


def _old_install(sub_brand: str = B.SUB_BRAND, markers=("voice:care-primary", "facts:ltc-info",
                                                        "keywords:care-division", "facts:care-division")) -> dict:
    """예전 버전으로 한동안 쓴 설치를 만든다 — 두 사업이 한 킷에 섞인 상태."""
    for suffix in ("", "-wal", "-shm"):
        path = Path(str(db.DB_PATH) + suffix)
        if path.exists():
            path.unlink()
    conn = sqlite3.connect(db.DB_PATH)
    conn.executescript(_OLD_BRAND_KIT_DDL)
    # brand_kit 말고는 지금 스키마와 같아도 됩니다(create table if not exists).
    conn.executescript(db.SCHEMA)
    pool = list(B.SEO_KEYWORDS) + [_USER_CARE_KW, _USER_HOUSE_KW]
    old = {
        "id": 1, "brand_name": B.BRAND_NAME, "sub_brand": sub_brand, "industry": B.INDUSTRY,
        "homepage": B.HOMEPAGE, "persona": B.PERSONA, "tone_and_manner": B.TONE_AND_MANNER,
        "naver_blog_id": "nanum_test", "instagram_handle": B.INSTAGRAM_HANDLE,
        "core_facts": json.dumps(list(B.CORE_FACTS) + [_USER_FACT], ensure_ascii=False),
        "few_shot_samples": "[]",
        "terminology": json.dumps(B.TERMINOLOGY, ensure_ascii=False),
        "seo_keywords": json.dumps(pool, ensure_ascii=False),
        "keyword_weights": json.dumps({"강서구 방문요양": 2.0, _USER_HOUSE_KW: 1.5}, ensure_ascii=False),
        "non_target_keywords": json.dumps(["가사관리사"], ensure_ascii=False),
        "service_areas": json.dumps(B.SERVICE_AREAS, ensure_ascii=False),
        "product_defaults": json.dumps(B.PRODUCT_DEFAULTS, ensure_ascii=False),
        "care_defaults": json.dumps(B.CARE_PRODUCT_DEFAULTS, ensure_ascii=False),
        "house_voice": json.dumps({
            "sub_brand": B.HOUSE_SUB_BRAND, "persona": "고친 가사 화자", "tone_and_manner": B.HOUSE_TONE,
            "few_shot_samples": B.HOUSE_FEW_SHOT, "service_areas": B.HOUSE_SERVICE_AREAS,
        }, ensure_ascii=False),
        "news_exclude_terms": json.dumps(B.NEWS_EXCLUDE_TERMS, ensure_ascii=False),
        "enabled_channels": json.dumps(["instagram", "daangn"]),
        "blacklist_map": json.dumps(B.BLACKLIST_MAP, ensure_ascii=False),
        "default_generation_vendor": "google", "vision_quality": "standard",
    }
    cols = ", ".join(old)
    conn.execute(f"insert into brand_kit ({cols}) values ({', '.join('?' * len(old))})", tuple(old.values()))
    for cid, post_type in (("c-care", "care"), ("c-house", "service"), ("c-free", None), ("c-tip", "tip")):
        conn.execute(
            "insert into campaigns (id, source_type, status, title, post_type) values (?, 'manual', 'draft', ?, ?)",
            (cid, cid, post_type),
        )
    conn.execute("insert into app_state (key, value) values ('sweep', ?)", (json.dumps({"stage": 2}),))
    conn.execute("insert into app_state (key, value) values ('brand_seed_fixes_applied', ?)",
                 (json.dumps({"done": list(markers)}),))
    conn.commit()
    conn.close()
    db._initialized = False
    db.init_db()
    seeded = B.seed_if_empty()
    B.apply_seed_fixes()
    return {"seeded": seeded}


def _kits():
    return {k["kit_key"]: repo.get_brand_kit(k["id"]) for k in repo.list_brand_kits()}


# --- 새 설치 -----------------------------------------------------------------

def test_fresh_install_seeds_two_kits():
    assert B.seed_if_empty() is True
    B.apply_seed_fixes()
    kits = repo.list_brand_kits()
    assert [k["name"] for k in kits] == [B.CARE_KIT_NAME, B.HOUSE_KIT_NAME]
    by_key = _kits()
    care, house = by_key["care"], by_key["house"]
    assert care["sub_brand"] == B.SUB_BRAND and house["sub_brand"] == B.HOUSE_SUB_BRAND
    assert any(f.startswith(B.INFO_FACT_PREFIX) for f in care["core_facts"])
    assert not any(f.startswith(B.INFO_FACT_PREFIX) for f in house["core_facts"])
    assert not set(B.HOUSE_FACTS) & set(care["core_facts"])
    assert set(B.HOUSE_FACTS) <= set(house["core_facts"])
    assert care["seo_keywords"] == B.CARE_SEO_KEYWORDS and house["seo_keywords"] == B.HOUSE_SEO_KEYWORDS
    assert care["product_defaults"] == B.CARE_PRODUCT_DEFAULTS and house["product_defaults"] == B.PRODUCT_DEFAULTS
    assert "02-6958-9084" in care["tone_and_manner"] and "02-2065-1584" in house["tone_and_manner"]
    # 회사 공통 값은 두 킷이 같습니다.
    assert care["brand_name"] == house["brand_name"] == B.BRAND_NAME
    assert care["blacklist_map"] == house["blacklist_map"]
    assert B.seed_if_empty() is False  # 두 번째 실행은 아무것도 안 함


def test_post_types_follow_kit():
    B.seed_if_empty()
    assert "care_guide" in post_types.for_kit("care") and "service" not in post_types.for_kit("care")
    assert "voucher" in post_types.for_kit("house") and "care" not in post_types.for_kit("house")
    assert "free" in post_types.for_kit("care") and "free" in post_types.for_kit("house")
    assert post_types.for_kit(None) == post_types.ORDER
    house = repo.get_brand_kit(repo.kit_id_for_key("house"))
    filled = post_types.default_product_fields("service", house, {})
    assert filled["price"] == B.PRODUCT_DEFAULTS["price"]
    care = repo.get_brand_kit(repo.kit_id_for_key("care"))
    # 가사 요금이 채워진 채로 돌봄 유형으로 바꾸면, 손대지 않은 기본값은 지웁니다.
    switched = post_types.default_product_fields("care", care, filled)
    assert not switched.get("price") and switched["order"] == B.CARE_PRODUCT_DEFAULTS["order"]


# --- 예전 한 킷 설치 -----------------------------------------------------------

def test_old_install_is_split_into_two_kits():
    result = _old_install()
    assert result["seeded"] is False
    by_key = _kits()
    care, house = by_key["care"], by_key["house"]
    assert care["id"] == 1  # 예전 킷의 ID를 이어받습니다
    assert care["name"] == B.CARE_KIT_NAME and house["name"] == B.HOUSE_KIT_NAME

    # 회사 공통·앱 설정으로 옮겨진 값
    company = repo.get_company_profile()
    assert company["naver_blog_id"] == "nanum_test" and company["news_exclude_terms"] == B.NEWS_EXCLUDE_TERMS
    app = repo.get_app_settings()
    assert app["default_generation_vendor"] == "google" and app["vision_quality"] == "standard"
    assert app["enabled_channels"] == ["instagram", "daangn"]

    # 화자: 돌봄센터는 그대로, 가사서비스는 house_voice(담당자가 고친 내용 포함)에서
    assert care["sub_brand"] == B.SUB_BRAND and care["persona"] == B.PERSONA
    assert care["industry"] == B.CARE_INDUSTRY and "가사" not in care["industry"]
    assert house["industry"] == B.HOUSE_INDUSTRY
    assert house["sub_brand"] == B.HOUSE_SUB_BRAND and house["persona"] == "고친 가사 화자"
    assert house["service_areas"] == B.HOUSE_SERVICE_AREAS and house["few_shot_samples"] == B.HOUSE_FEW_SHOT

    # 팩트: 사업별로 나뉘고, 어느 쪽인지 모르는 담당자 팩트는 두 킷 모두에
    assert any(f.startswith(B.INFO_FACT_PREFIX) for f in care["core_facts"])
    assert not set(B.HOUSE_FACTS) & set(care["core_facts"])
    assert not any(f.startswith(B.INFO_FACT_PREFIX) for f in house["core_facts"])
    assert set(B.HOUSE_FACTS) <= set(house["core_facts"]) and not set(B.CARE_FACTS[1:]) & set(house["core_facts"])
    assert _USER_FACT in care["core_facts"] and _USER_FACT in house["core_facts"]

    # 용어집
    assert "우렁각시 홈서비스" in house["terminology"] and "우렁각시 홈서비스" not in care["terminology"]
    assert "송영" in care["terminology"] and "송영" not in house["terminology"]
    assert "강서나눔돌봄센터" in care["terminology"] and "강서나눔돌봄센터" in house["terminology"]

    # 키워드: 담당자가 더한 동네 키워드까지 사업별로, 가중치·타깃 해제도 따라감
    assert _USER_CARE_KW in care["seo_keywords"] and _USER_CARE_KW not in house["seo_keywords"]
    assert _USER_HOUSE_KW in house["seo_keywords"] and _USER_HOUSE_KW not in care["seo_keywords"]
    assert set(B.CARE_SEO_KEYWORDS) <= set(care["seo_keywords"])
    assert set(B.HOUSE_SEO_KEYWORDS) <= set(house["seo_keywords"])
    assert house["keyword_weights"] == {_USER_HOUSE_KW: 1.5}
    assert care["keyword_weights"] == {"강서구 방문요양": 2.0}
    assert house["non_target_keywords"] == ["가사관리사"] and care["non_target_keywords"] == []

    # 서비스 기본값
    assert care["product_defaults"] == B.CARE_PRODUCT_DEFAULTS and house["product_defaults"] == B.PRODUCT_DEFAULTS

    # 글은 글 유형으로 킷이 정해짐 — [가사] 유형은 가사서비스 킷
    kit_of = {c["id"]: c["brand_kit_id"] for c in repo.list_campaigns()}
    assert kit_of == {"c-care": care["id"], "c-house": house["id"], "c-free": care["id"], "c-tip": house["id"]}
    assert repo.get_campaign("c-house")["brand_kit_name"] == B.HOUSE_KIT_NAME

    # 키워드 화면 진행 상태는 첫 킷(돌봄센터)의 것으로
    assert repo.get_app_state(repo.kit_state_key("sweep", care["id"])) == {"stage": 2}
    assert repo.get_app_state("sweep") is None


def test_split_runs_once_and_keeps_later_edits():
    _old_install()
    house_id = repo.kit_id_for_key("house")
    repo.save_brand_kit(house_id, persona="나중에 다시 고친 화자")
    db._initialized = False
    db.init_db()
    B.seed_if_empty()
    B.apply_seed_fixes()
    assert len(repo.list_brand_kits()) == 2
    assert repo.get_brand_kit(house_id)["persona"] == "나중에 다시 고친 화자"


def test_very_old_install_still_house_voice():
    """돌봄 사업을 더하기 전 버전(기본 화자 = 가사서비스)에서 바로 올라온 설치."""
    _old_install(sub_brand=B.HOUSE_SUB_BRAND, markers=())
    by_key = _kits()
    care, house = by_key["care"], by_key["house"]
    assert care["sub_brand"] == B.SUB_BRAND and care["persona"] == B.PERSONA
    assert house["sub_brand"] == B.HOUSE_SUB_BRAND
    assert set(B.CARE_SEO_KEYWORDS) <= set(care["seo_keywords"])
    assert all(f in care["core_facts"] for f in B.INFO_FACTS)


# --- 킷 관리 -------------------------------------------------------------------

def test_campaign_uses_its_kit_and_company_values():
    B.seed_if_empty()
    house_id = repo.kit_id_for_key("house")
    camp = repo.insert_campaign(source_type="manual", memo="정리수납", brand_kit_id=house_id)
    kit = repo.get_campaign_brand_kit(camp)
    assert kit["id"] == house_id and kit["sub_brand"] == B.HOUSE_SUB_BRAND
    assert kit["naver_blog_id"] == B.NAVER_BLOG_ID and kit["guardrail_enabled"] is True
    assert camp["brand_kit_name"] == B.HOUSE_KIT_NAME
    default = repo.insert_campaign(source_type="manual")
    assert default["brand_kit_id"] == repo.kit_id_for_key("care")


def test_names_archive_restore():
    B.seed_if_empty()
    care_id, house_id = repo.kit_id_for_key("care"), repo.kit_id_for_key("house")
    with pytest.raises(repo.BrandKitError):
        repo.save_brand_kit(house_id, name=B.CARE_KIT_NAME)
    copy_id = repo.create_brand_kit("돌봄 복사", copy_from=care_id)
    copy = repo.get_brand_kit(copy_id)
    assert copy["persona"] == B.PERSONA and copy["kit_key"] is None  # 복제한 킷은 표시가 없음
    camp = repo.insert_campaign(source_type="manual", brand_kit_id=house_id)
    moved = repo.archive_brand_kit(house_id, move_unpublished_to=care_id)
    assert moved == 1 and repo.get_campaign(camp["id"])["brand_kit_id"] == care_id
    assert repo.kit_id_for_key("house") is None
    assert repo.restore_brand_kit(house_id) == B.HOUSE_KIT_NAME
    repo.archive_brand_kit(copy_id)
    repo.archive_brand_kit(house_id)
    with pytest.raises(repo.BrandKitError):
        repo.archive_brand_kit(care_id)  # 마지막 남은 킷


def test_append_tone_rule_goes_to_that_kit():
    B.seed_if_empty()
    house_id = repo.kit_id_for_key("house")
    assert repo.append_tone_rule("가격은 표로 정리합니다", kit_id=house_id)
    assert "가격은 표로 정리합니다" in repo.get_brand_kit(house_id)["tone_and_manner"]
    assert "가격은 표로 정리합니다" not in repo.get_brand_kit(repo.kit_id_for_key("care"))["tone_and_manner"]
