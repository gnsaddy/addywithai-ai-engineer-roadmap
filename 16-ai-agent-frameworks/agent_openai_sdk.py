# agent_openai_sdk.py: the Episode 15 agent, built with the OpenAI Agents SDK.
# You describe the agent. The SDK's Runner runs the loop for you.
from agents import (Agent, OpenAIChatCompletionsModel, Runner,
                    function_tool, set_tracing_disabled)
from openai import AsyncOpenAI
from settings import API_KEY, BASE_URL, MODEL, QUESTIONS, SYSTEM
import tools

set_tracing_disabled(True)   # tracing uploads to OpenAI; off for local runs
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

agent = Agent(
    name="Travel helper",
    instructions=SYSTEM,
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    tools=[function_tool(tools.search_policy),     # schemas come from
           function_tool(tools.calculator)],       # the functions
)

def run_agent(question, max_steps=6):
    result = Runner.run_sync(agent, question, max_turns=max_steps)
    for item in result.new_items:                  # what the loop did
        if item.type == "tool_call_item":
            print(f"  act: {item.raw_item.name}({item.raw_item.arguments})")
        elif item.type == "tool_call_output_item":
            print(f"  see: {str(item.output)[:64]}")
    return result.final_output

if __name__ == "__main__":
    for q in QUESTIONS:
        print("Q:", q)
        print("A:", run_agent(q), "\n")
