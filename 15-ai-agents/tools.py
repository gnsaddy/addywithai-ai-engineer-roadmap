# tools.py: the agent's two tools, plus their JSON schemas for the model.
import ast, operator as op

POLICY = [
    "The hotel limit is 150 US dollars per night.",
    "In London, New York and Tokyo the hotel limit is 250 US dollars per night.",
    "Meals are covered up to 60 US dollars per day.",
    "Submit your expense claim within 30 days of the trip.",
]

def search_policy(query):
    """Return the 2 policy sentences that share the most words with the query."""
    words = set(query.lower().split())
    score = lambda s: len(words & set(s.lower().rstrip(".").split()))
    return " ".join(sorted(POLICY, key=score, reverse=True)[:2])

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}

def calculator(expression):
    """Safely work out + - * / on numbers. No eval()."""
    def run(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](run(n.left), run(n.right))
        raise ValueError("only numbers and + - * /")
    return str(run(ast.parse(expression, mode="eval").body))

TOOLS = {"search_policy": search_policy, "calculator": calculator}
