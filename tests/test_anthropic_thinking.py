"""Claude 5세대의 생각(thinking) 토큰이 출력 한도를 다 써서 글·사진 설명이 잘리던 문제."""
from types import SimpleNamespace

import pytest


def _response(text="본문", stop_reason="end_turn", output_tokens=50, category=None):
    return SimpleNamespace(
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        stop_details=SimpleNamespace(category=category) if category else None,
        usage=SimpleNamespace(input_tokens=10, output_tokens=output_tokens,
                              cache_read_input_tokens=0, cache_creation_input_tokens=0),
    )


def _fake_anthropic(monkeypatch, response):
    sent = []

    class FakeMessages:
        def create(self, **kw):
            sent.append(kw)
            return response

    class FakeClient:
        def __init__(self, api_key):
            self.messages = FakeMessages()

    import anthropic
    monkeypatch.setattr(anthropic, "Anthropic", FakeClient)
    return sent


@pytest.mark.parametrize("model", ["claude-sonnet-5-5", "claude-sonnet-5", "claude-opus-5-5",
                                   "claude-fable-5-1", "claude-haiku-5-5", "Claude-Sonnet-5-5"])
def test_thinking_models_get_room_to_think(model):
    from ai_workers.multi_llm_router import _REASONING_HEADROOM, anthropic_request_options
    opts = anthropic_request_options(model, 900)
    assert opts["max_tokens"] == 900 + _REASONING_HEADROOM
    assert opts["output_config"] == {"effort": "medium"}


@pytest.mark.parametrize("model", ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001", "", None])
def test_older_models_are_sent_unchanged(model):
    # 4세대 이하는 기본이 생각 꺼짐이고, Haiku 4.5 등은 effort를 보내면 오류가 납니다.
    from ai_workers.multi_llm_router import anthropic_request_options
    assert anthropic_request_options(model, 900) == {"max_tokens": 900}


def test_text_call_sends_headroom_and_returns_only_text(monkeypatch):
    from ai_workers import multi_llm_router as r
    sent = _fake_anthropic(monkeypatch, _response("완성된 본문"))
    text, _in, _out, truncated = r._call_anthropic("claude-sonnet-5-5", "k", "프롬프트", "시스템", 4000)
    assert text == "완성된 본문" and truncated is False
    assert sent[0]["max_tokens"] == 4000 + r._REASONING_HEADROOM
    assert sent[0]["output_config"] == {"effort": "medium"}


def test_refusal_is_raised_not_saved_as_a_finished_draft(monkeypatch):
    from ai_workers import multi_llm_router as r
    _fake_anthropic(monkeypatch, _response("중간까지 쓴 글", stop_reason="refusal", category="bio"))
    with pytest.raises(RuntimeError, match="중단"):
        r._call_anthropic("claude-sonnet-5-5", "k", "프롬프트", None, 4000)


def test_vision_call_sends_headroom_and_skips_thinking_blocks(monkeypatch):
    from ai_workers import vision
    from ai_workers.multi_llm_router import _REASONING_HEADROOM
    sent = _fake_anthropic(monkeypatch, _response('{"captions": ["사진 설명"]}'))
    text, _in, _out = vision._call_anthropic("claude-sonnet-5-5", "k", [b"\xff\xd8jpeg"], 100)
    assert text == '{"captions": ["사진 설명"]}'
    assert sent[0]["max_tokens"] == 100 + _REASONING_HEADROOM
