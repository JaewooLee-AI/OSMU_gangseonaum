"""OpenAI 호출 파라미터 — gpt-5 이후 모델은 max_tokens를 거부한다(2026-10-21 사진 분석 전면 실패)."""
import sys
import types


def _fake_openai(captured):
    class _Completions:
        def create(self, **kw):
            captured.update(kw)
            msg = types.SimpleNamespace(content='{"captions": ["a"]}')
            choice = types.SimpleNamespace(message=msg, finish_reason="stop")
            usage = types.SimpleNamespace(prompt_tokens=10, completion_tokens=5)
            return types.SimpleNamespace(choices=[choice], usage=usage)

    class OpenAI:
        def __init__(self, api_key=None):
            self.chat = types.SimpleNamespace(completions=_Completions())

    return types.SimpleNamespace(OpenAI=OpenAI)


def test_vision_openai_uses_max_completion_tokens(monkeypatch):
    from ai_workers import vision
    captured = {}
    monkeypatch.setitem(sys.modules, "openai", _fake_openai(captured))
    vision._call_openai("gpt-5-mini", "k", [b"\xff\xd8"], 300)
    assert "max_tokens" not in captured
    assert captured["max_completion_tokens"] > 300  # 추론 여유분 포함


def test_reasoning_detection_covers_new_generations():
    from ai_workers.multi_llm_router import _is_openai_reasoning_model, openai_output_ceiling
    for m in ("gpt-5-mini", "gpt-5.4-mini", "gpt-6-luna", "gpt-6.1-sol", "o3", "o4-mini"):
        assert _is_openai_reasoning_model(m), m
    for m in ("gpt-4.1-mini", "gpt-4o"):
        assert not _is_openai_reasoning_model(m), m
    assert openai_output_ceiling("gpt-4.1-mini", 100) == 100
