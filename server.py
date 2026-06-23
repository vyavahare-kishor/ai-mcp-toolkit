from mcp.server.fastmcp import FastMCP
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

# FastMCP — the high-level framework on top of the raw MCP protocol.
# Each @mcp.tool() function becomes a tool any MCP client can discover and call.
mcp = FastMCP("ai-toolkit")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@mcp.tool()
def web_research(topic: str) -> str:
    """Search the web for current information on a topic and return a
    concise summary with key points drawn from the results."""
    response = tavily_client.search(topic, max_results=3)
    results = response.get("results", [])

    if not results:
        return "No results found."

    context = "\n\n".join(f"{r['title']}: {r['content']}" for r in results)

    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Summarize these search results into 3-4 key points with sources."},
            {"role": "user", "content": context}
        ],
        max_tokens=400
    )
    return completion.choices[0].message.content


@mcp.tool()
def review_code_diff(diff: str, focus: str = "bugs and code quality") -> str:
    """Review a code diff and return structured, actionable feedback.
    Pass raw diff text. Optionally specify a focus area like 'security'."""
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are a senior code reviewer. Focus on {focus}. Be specific and actionable, reference actual lines."},
            {"role": "user", "content": f"Review this diff:\n\n{diff}"}
        ],
        max_tokens=600
    )
    return completion.choices[0].message.content


@mcp.tool()
def explain_concept(concept: str, audience: str = "a senior backend engineer new to AI") -> str:
    """Explain a technical or AI concept tailored to a specific audience's
    background level, using concrete analogies."""
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"Explain concepts clearly for {audience}. Use concrete analogies they'd already understand."},
            {"role": "user", "content": f"Explain: {concept}"}
        ],
        max_tokens=500
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    mcp.run()
