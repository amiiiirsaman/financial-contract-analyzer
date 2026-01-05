import boto3
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .smart_router import get_model_for_query, REGION


@dataclass
class RAGConfig:
    knowledge_base_id: str
    guardrail_id: Optional[str] = None
    guardrail_version: Optional[str] = None
    max_tokens: int = 512
    top_k: int = 5


class RAGService:
    def __init__(self, config: RAGConfig):
        self.config = config
        self._agent_runtime = boto3.client(
            "bedrock-agent-runtime",
            region_name=REGION,
        )

    def _build_model_arn(self, model_id: str) -> str:
        return f"arn:aws:bedrock:{REGION}::foundation-model/{model_id}"

    def _build_retrieve_and_generate_config(self, model_arn: str) -> Dict[str, Any]:
        base_cfg: Dict[str, Any] = {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": self.config.knowledge_base_id,
                "modelArn": model_arn,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {
                        "numberOfResults": self.config.top_k
                    }
                },
            },
        }
    
        if self.config.guardrail_id and self.config.guardrail_version:
            base_cfg["guardrailConfiguration"] = {
                "guardrailId": self.config.guardrail_id,
                "guardrailVersion": self.config.guardrail_version,
            }
    
        # REMOVE the inferenceConfig block entirely
        return base_cfg

    def get_response(self, query: str, session_id: str | None = None) -> str:
        model_id = get_model_for_query(query)
        model_arn = self._build_model_arn(model_id)
    
        params: Dict[str, Any] = {
            "input": {"text": query},
            "retrieveAndGenerateConfiguration": self._build_retrieve_and_generate_config(
                model_arn
            ),
        }
        # REMOVE use of sessionId
        # if session_id:
        #     params["sessionId"] = session_id
    
        resp = self._agent_runtime.retrieve_and_generate(**params)
        return resp["output"]["text"]

