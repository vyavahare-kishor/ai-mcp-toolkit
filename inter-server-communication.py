import httpx
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

RESEARCH_AGENT_URL = os.getenv("RESEARCH_AGENT_URL", "http://localhost:8003")
PR_REVIEWER_URL = os.getenv("PR_REVIEWER_URL", "http://localhost:8004")


@mcp.tool()
def web_research(topic: str, depth: str = "quick") -> str:
    """Run the ai-research-agent service's autonomous web research agent on a topic.
    depth: 'quick', 'medium', or 'deep'."""
    response = httpx.post(
        f"{RESEARCH_AGENT_URL}/research/",
        json={"topic": topic, "depth": depth},
        timeout=120
    )
    response.raise_for_status()
    data = response.json()
    findings = "\n".join(f"- {f}" for f in data.get("key_findings", []))
    return f"{data.get('summary', '')}\n\nKey findings:\n{findings}"


@mcp.tool()
def review_pr(pr_url: str, focus: str = None) -> str:
    """Run the ai-pr-reviewer service's AI code review on a real GitHub PR URL."""
    payload = {"pr_url": pr_url}
    if focus:
        payload["focus"] = focus

    response = httpx.post(
        f"{PR_REVIEWER_URL}/pr-review/", json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    issues = "\n".join(
        f"- [{i['severity']}] {i['file']}: {i['description']}"
        for i in data.get("issues", [])
    )
    verdict = "Approved" if data["approved"] else "Changes requested"
    return f"Score: {data['overall_score']}/10 — {verdict}\n\n{data['summary']}\n\nIssues:\n{issues}"


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
