Financial Contract Analyzer
A production-ready Retrieval-Augmented Generation (RAG) application for analyzing financial contracts using Amazon Bedrock, intelligent model routing, and cost optimization.

Overview
Financial Contract Analyzer combines:

Amazon Bedrock Knowledge Bases for vector-indexed contract retrieval from S3

Smart Model Router that dynamically routes queries between Claude 3 Haiku (fast, cost-effective) and Claude 3.5 Sonnet (complex reasoning)

Streamlit UI for interactive contract analysis

Production-ready code with logging, error handling, and testing

This capstone demonstrates enterprise AI architecture patterns: RAG systems, multi-model routing for cost optimization, and serverless deployment on AWS.

Architecture
User Query (Streamlit UI)
        ↓
    RAG Service
        ↓
    Smart Router (classify complexity)
        ├─→ Simple Query → Haiku ($0.80/$2.40 per MTok)
        └─→ Complex Query → Sonnet ($3/$15 per MTok)
        ↓
Bedrock RetrieveAndGenerate
        ↓
Knowledge Base (OpenSearch Serverless + S3)
        ↓
Grounded Answer (with citations from contracts)



Key benefits:

Cost-aware: Haiku handles ~70% of queries at 1/3 the cost of Sonnet

Accurate: RAG grounds answers in actual contract text

Scalable: Serverless on AWS; no infrastructure to manage

Maintainable: Clean service layer + comprehensive logging

Features
✅ Smart Model Routing: Keyword-based complexity classifier (compare, analyze, summarize → Sonnet; simple fact lookups → Haiku)

✅ RAG with Bedrock Knowledge Bases: Retrieves relevant contract sections before generation

✅ Session-aware context: Conversation history ready for multi-turn interactions

✅ Error handling: Graceful fallbacks for Bedrock errors

✅ GitHub Actions CI/CD: Linting (flake8) and testing (pytest) on every push

✅ Professional logging: Tracks model routing decisions and errors

✅ **Optional Guardr

