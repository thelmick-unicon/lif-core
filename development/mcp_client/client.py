"""
This module provides a command-line client for performing semantic search queries
using the lif_query tool via the MCP (Model Control Plane) service.

It initializes a filter for person identification, sets up the MCP client using
the provided TOOL_URL environment variable (defaulting to http://localhost:8003/mcp),
and enters an interactive loop where the user can input semantic search queries.
Results are printed to the console.

Main components:
- Filter setup for person identification.
- Asynchronous client connection to the MCP service.
- Interactive prompt for user queries.
- Result formatting and display.

Usage:
    python client.py

Environment Variables:
    TOOL_URL: The URL of the MCP service endpoint (default: http://localhost:8003/mcp).
"""

import asyncio
import logging
import os
from typing import Any

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from rich.logging import RichHandler

# --- Logging Setup with Rich ---
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger("lif_query")  # You can use __name__ if you prefer

TOOL_URL = os.environ.get("LIF_SEMANTIC_SEARCH_MCP_SERVER_URL", "http://localhost:8003/mcp")
LLM_MODEL_NAME = os.environ.get("LIF_ADVISOR_LLM_MODEL_NAME", "gpt-4.1-mini")


async def ask_agent(agent: Any, message: str) -> str:
    if agent is None:
        logger.error("Agent not initialized! Call setup_agent() first.")
        raise Exception("Agent not initialized! Call setup_agent() first.")
    result = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
    messages = result.get("messages", [])
    final_message = messages[len(messages) - 1]
    return final_message.content


def print_result(result):
    logger.info("--- lif_query result ---")
    for item in result:
        logger.info(f"Type: {type(item)}")
        if hasattr(item, "text"):
            logger.info(item.text)
        else:
            logger.info(item)


async def query_loop(agent: Any):
    while True:
        try:
            prompt = input("\nEnter your semantic search query (empty to exit): ").strip()
        except (KeyboardInterrupt, EOFError):
            logger.info("Exiting.")
            break
        if not prompt:
            logger.info("Goodbye!")
            break
        result = await ask_agent(agent, prompt)
        logger.info(result)


async def main():
    client = MultiServerMCPClient({"lif-mcp-tool": {"url": TOOL_URL, "transport": "streamable_http"}})

    tools = await client.get_tools()

    agent = create_react_agent(ChatOpenAI(model=LLM_MODEL_NAME), tools, debug=LOG_LEVEL == "DEBUG")

    await query_loop(agent)


if __name__ == "__main__":
    asyncio.run(main())
