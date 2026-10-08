"""OPTIONAL: expose the support bot as an MCP server (tools other AI clients can call).
Run: python mcp_server.py     (needs `pip install "mcp<2"`)"""
from mcp.server.fastmcp import FastMCP

from rag_agent import retrieve_policies, support_bot

mcp = FastMCP("acme-support")


@mcp.tool()
def lookup_policy(question: str) -> list[str]:
    """Return the policy snippets most relevant to a question."""
    return retrieve_policies(question)


@mcp.tool()
def ask_support_bot(question: str) -> str:
    """Answer a customer-support question using the policy knowledge base."""
    return support_bot(question)[0]


if __name__ == "__main__":
    mcp.run()
