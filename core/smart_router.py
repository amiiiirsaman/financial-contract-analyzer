import boto3
from typing import Literal
import json

REGION = "us-east-1"

HAIKU_ID = "anthropic.claude-3-haiku-20240307-v1:0"
SONNET_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

Complexity = Literal["SIMPLE", "COMPLEX"]

bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)


def classify_query_complexity(query: str) -> Complexity:
    complex_keywords = [
        "compare", "contrast", "summarize", "summary",
        "analyze", "analysis", "explain", "advantages",
        "disadvantages", "pros and cons", "impact", "implications",
    ]
    q_lower = query.lower()
    if any(kw in q_lower for kw in complex_keywords):
        return "COMPLEX"
    return "SIMPLE"


def get_model_for_query(query: str) -> str:
    complexity = classify_query_complexity(query)
    if complexity == "SIMPLE":
        print("Routing to: Haiku (simple query)")
        return HAIKU_ID
    print("Routing to: Sonnet (complex query)")
    return SONNET_ID


def invoke_model(model_id: str, prompt: str) -> str:
    body = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.2,
    }
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(body).encode("utf-8"),
    )
    return response["body"].read().decode("utf-8")
