import types

from core.rag_service import RAGService, RAGConfig


class FakeClient:
    def __init__(self):
        self.last_kwargs = None

    def retrieve_and_generate(self, **kwargs):
        self.last_kwargs = kwargs
        return {"output": {"text": "stubbed response"}}


def test_rag_service_builds_config(monkeypatch):
    cfg = RAGConfig(
        knowledge_base_id="KB123",
        guardrail_id="GR1",
        guardrail_version="1",
        max_tokens=256,
        top_k=3,
    )
    service = RAGService(cfg)

    fake = FakeClient()
    service._agent_runtime = fake  # type: ignore[attr-defined]

    # monkeypatch router
    import core

    def fake_router(_q: str) -> str:
        return "anthropic.claude-3-haiku-20240307-v1:0"

    core.smart_router.get_model_for_query = fake_router  # type: ignore

    out = service.get_response("What is the term?", "sess1")
    assert out == "stubbed response"
    assert fake.last_kwargs["sessionId"] == "sess1"
    assert fake.last_kwargs["retrieveAndGenerateConfiguration"][
        "knowledgeBaseConfiguration"
    ]["knowledgeBaseId"] == "KB123"
