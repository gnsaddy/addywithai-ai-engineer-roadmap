# server.py: a small MCP server with 2 tools and 1 resource.
# Any MCP host (Claude Desktop, VS Code, your own agent) can use it.
import ast, operator as op, sys
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("travel-policy")     # the server's name

POLICY = [
    "The hotel limit is 150 US dollars per night.",
    "In London, New York and Tokyo the hotel limit is 250 US dollars per night.",
    "Meals are covered up to 60 US dollars per day.",
    "Submit your expense claim within 30 days of the trip.",
]

@mcp.tool()
def search_policy(query: str) -> str:
    """Search the company travel policy. Example query: hotel limit Tokyo"""
    words = set(query.lower().split())
    score = lambda s: len(words & set(s.lower().rstrip(".").split()))
    return " ".join(sorted(POLICY, key=score, reverse=True)[:2])

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}

@mcp.tool()
def calculator(expression: str) -> str:
    """Do maths with + - * / on numbers. Example: 3 * 250 + 3 * 60"""
    def run(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](run(n.left), run(n.right))
        raise ToolError("only numbers and + - * /")   # the model reads this
    if len(expression) > 100:                  # never trust the input
        raise ToolError("expression too long")
    return str(run(ast.parse(expression, mode="eval").body))

@mcp.resource("policy://travel")
def full_policy() -> str:
    """The full travel policy, as read-only text."""
    return "\n".join(POLICY)

if __name__ == "__main__":
    if "--http" in sys.argv:         # remote style: http://127.0.0.1:8000/mcp
        mcp.run(transport="streamable-http")
    else:                            # local style: stdin and stdout
        mcp.run()
