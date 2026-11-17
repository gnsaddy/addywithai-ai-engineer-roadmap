# schemas.py: how we describe the two tools to the model (OpenAI tool format).
def tool(name, about, arg, arg_about):
    return {"type": "function", "function": {
        "name": name, "description": about,
        "parameters": {"type": "object", "required": [arg],
                       "properties": {arg: {"type": "string",
                                            "description": arg_about}}}}}

SCHEMAS = [
    tool("search_policy", "Search the company travel policy.",
         "query", "what to look for, e.g. hotel limit Tokyo"),
    tool("calculator", "Do maths with + - * / on numbers.",
         "expression", "e.g. 3 * 250 + 3 * 60"),
]
