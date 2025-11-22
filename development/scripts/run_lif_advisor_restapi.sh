#!/bin/bash
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: The OPENAI_API_KEY environment variable is not set."
    echo "Please set OPENAI_API_KEY and re-run this script."
    exit 1
fi

export LIF_SEMANTIC_SEARCH_MCP_SERVER_URL=http://localhost:8003/mcp
export LIF_GRAPHQL_API_URL=http://localhost:8000/graphql
export LIF_ADVISOR_AGENT_TASKS=load_profile,continue_conversation,save_interaction_summary
export LIF_ADVISOR_LLM_MODEL_NAME=gpt-4.1-mini
export LIF_ADVISOR_MESSAGES_TO_KEEP=4
export LIF_ADVISOR_TRIMMED_MESSAGES_SIZE=384
export LIF_ADVISOR_MAX_CONVERSATION_SIZE=2048
export LIF_ADVISOR_MAX_SUMMARY_SIZE=1024

uv run uvicorn lif.advisor_restapi.core:app --host 0.0.0.0 --port 8004
