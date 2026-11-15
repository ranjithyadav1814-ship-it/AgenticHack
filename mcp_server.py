"""Instructor demo: expose the Intro Build calculator over MCP."""
import os
from getpass import getpass

if not os.environ.get('GROQ_API_KEY'):
    os.environ['GROQ_API_KEY'] = getpass('Groq API key: ').strip()

from langchain_groq import ChatGroq
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

model = ChatGroq(model="openai/gpt-oss-20b", temperature=0, timeout=30, max_retries=1)

from langchain.tools import tool
mcp = FastMCP(
    "Intelligent Calculator",
    host=os.environ.get("INTRO_MCP_HOST", "127.0.0.1"),
    stateless_http=True,
    json_response=True,
)

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def solve_math_problem(problem: str) -> str:
    """Solve an apples addition or tree-distance word problem. Pass the original wording."""
    problem = problem.strip()
    if not 1 <= len(problem) <= 1500:
        return "Enter an English word problem of 1 to 1500 characters."
    result = agent.invoke(
        {"messages": [("human", problem)]},
        config={"recursion_limit": 8, "run_name": "intro_calculator_mcp"},
    )
    return result["messages"][-1].text

if __name__ == "__main__":
    mcp.run(transport="streamable-http")