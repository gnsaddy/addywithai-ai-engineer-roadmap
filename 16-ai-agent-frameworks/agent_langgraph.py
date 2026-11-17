# agent_langgraph.py: the Episode 15 agent, built with LangGraph.
# You draw the loop as a graph: a model node, a tools node, and edges.
from langchain_core.messages import AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from settings import API_KEY, BASE_URL, MODEL, QUESTIONS, SYSTEM
from tools import calculator, search_policy

TOOLS = [search_policy, calculator]
llm = ChatOpenAI(model=MODEL, base_url=BASE_URL, api_key=API_KEY)
llm = llm.bind_tools(TOOLS)          # schemas come from the functions

def call_model(state: MessagesState):                     # Reason
    return {"messages": [llm.invoke(state["messages"])]}

graph = StateGraph(MessagesState)    # the state is the list of messages
graph.add_node("model", call_model)
graph.add_node("tools", ToolNode(TOOLS))                  # Act
graph.add_edge(START, "model")
graph.add_conditional_edges("model", tools_condition)     # tool call or END?
graph.add_edge("tools", "model")                          # Observe, go again
agent = graph.compile()

def run_agent(question, max_steps=6):
    start = {"messages": [("system", SYSTEM), ("user", question)]}
    limit = {"recursion_limit": 2 * max_steps + 1}        # the step limit
    for update in agent.stream(start, limit, stream_mode="updates"):
        for msg in [m for part in update.values() for m in part["messages"]]:
            if isinstance(msg, AIMessage) and msg.tool_calls:
                for c in msg.tool_calls:
                    arg = next(iter(c["args"].values()), "")
                    print(f"  act: {c['name']}({arg!r})")
            elif isinstance(msg, ToolMessage):
                print(f"  see: {msg.content[:64]}")
            else:
                return msg.content

if __name__ == "__main__":
    for q in QUESTIONS:
        print("Q:", q)
        print("A:", run_agent(q), "\n")
