"""2026-11-03 실제 생성에서 찾은 글 품질 문제 세 가지의 시험 — LLM 없이.

1. 제목에 소재와 무관한 키워드를 강제 ('장기요양등급 활용으로 만난 가을 단풍 그리기 시간')
2. 메모에 없는 어르신의 말을 인용으로 지어냄
3. 키워드 밀도를 채우려 '전문 가사도우미 손길이 필요한 … 관리사님'처럼 끼워 넣음
"""
from __future__ import annotations

from ai_workers import seo_optimizer as S
from ai_workers import content_writer as W
from ai_workers.content_writer import invented_quotes

AREAS = ["강서구", "화곡동", "마곡동"]


def test_title_keywords_must_match_subject():
    memo = "이번 주 실버미술 시간에 어르신들이 가을 단풍을 그리셨습니다."
    pool = ["장기요양등급", "강서구 주간보호센터", "실버미술"]
    assert S.subject_keywords(pool, memo, AREAS) == ["실버미술"]


def test_subject_match_allows_area_and_generic_suffix():
    memo = "화곡동 주간보호 이용 문의가 늘었습니다. 장기요양등급 신청 방법도 자주 묻습니다."
    pool = ["강서구 주간보호센터", "장기요양등급신청", "장기요양등급신청방법", "가사도우미", "서울형 가사서비스"]
    assert S.subject_keywords(pool, memo, AREAS) == ["강서구 주간보호센터", "장기요양등급신청", "장기요양등급신청방법"]


def test_house_memo_does_not_pull_voucher_keyword():
    memo = "정기 3시간 가사서비스를 처음 신청하는 맞벌이 가정이 늘었습니다."
    pool = ["서울형 가사서비스", "가사도우미", "가사서비스", "강서구 가사도우미"]
    assert S.subject_keywords(pool, memo, AREAS) == ["가사서비스"]


def test_empty_subject_allows_nothing():
    assert S.subject_keywords(["가사서비스"], "", AREAS) == []


def test_invented_quote_is_reported():
    body = (
        "화곡동에 사시는 80대 어르신은 그림을 한참 바라보셨습니다.\n"
        "“손이 마음대로 안 움직일 줄 알았는데, 이렇게 다 그리고 나니 참 곱네.”\n"
        "이번 프로그램의 이름은 '실버미술'입니다."
    )
    memo = "실버미술 시간에 단풍을 그렸습니다. 처음엔 붓 잡기를 망설이시던 분도 끝까지 완성하셨어요."
    assert invented_quotes(body, [memo]) == ["손이 마음대로 안 움직일 줄 알았는데, 이렇게 다 그리고 나니 참 곱네."]


def test_quote_from_memo_or_article_is_fine():
    memo = '어르신 한 분이 "오늘 그림이 제일 마음에 든다"고 하셨어요.'
    body = "그날 어르신은 “오늘 그림이 제일 마음에 든다”고 말씀하셨습니다."
    assert invented_quotes(body, [memo]) == []
    article = "장관은 \"돌봄 인력 처우를 개선하겠다\"고 밝혔다."
    assert invented_quotes("정부는 \"돌봄 인력 처우를 개선하겠다\"고 밝혔습니다.", ["", article]) == []


def test_rebalance_passes_style_rules(monkeypatch):
    seen = {}

    def fake(vendor, prompt, system, max_tokens, note):
        seen["prompt"], seen["system"] = prompt, system
        return "가사도우미 " * 3 + "본문입니다. " * 40

    monkeypatch.setattr(S, "generate_text", fake)
    S.rebalance_keywords("제목", "본문입니다. " * 40, ["가사도우미"], "google",
                         style_rules="- '가사도우미'는 한 글에 한두 번만 씁니다.")
    assert "[문체 규칙" in seen["prompt"] and "한두 번만" in seen["prompt"]
    assert "꾸미는 말로 끼워 넣거나" in seen["system"]


def test_invented_quotes_are_rewritten_by_paragraph(monkeypatch):
    body = ("그림 시간이 시작됐습니다.\n\n“손이 굳어서 잘 못 그릴 것 같아요.”\n\n"
            "한 분은 \"내가 그림을 그려 본 적이 없는데 어쩌나\"라며 붓을 내려놓으셨어요. 그래도 끝까지 완성하셨습니다.")
    quotes = invented_quotes(body, ["붓 잡기를 망설이시던 분도 끝까지 완성하셨어요."])
    assert quotes == ["손이 굳어서 잘 못 그릴 것 같아요.", "내가 그림을 그려 본 적이 없는데 어쩌나"]
    reply = ('{"paragraphs": [{"n": 1, "text": "처음엔 붓 잡기를 망설이셨어요."}, '
             '{"n": 2, "text": "한 분은 처음에 붓을 내려놓고 망설이셨어요. 그래도 끝까지 완성하셨습니다."}]}')
    monkeypatch.setattr(W, "generate_text", lambda **kw: reply)
    new, fixed = W.rewrite_invented_quotes(body, quotes, "메모", "google", {})
    assert fixed == quotes
    assert "“" not in new and '"' not in new and "그래도 끝까지 완성하셨습니다." in new
    assert new.count("\n") == body.count("\n")


def test_rewrite_rejected_when_it_drops_content(monkeypatch):
    body = "한 분은 \"내가 그림을 그려 본 적이 없는데 어쩌나\"라며 붓을 내려놓으셨어요. 그래도 끝까지 완성하셨고 보호자분도 좋아하셨습니다."
    quotes = invented_quotes(body, [""])
    monkeypatch.setattr(W, "generate_text", lambda **kw: '{"paragraphs": [{"n": 1, "text": "망설이셨어요."}]}')
    new, fixed = W.rewrite_invented_quotes(body, quotes, "메모", "google", {})
    assert new == body and fixed == []
