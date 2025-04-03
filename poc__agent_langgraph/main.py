"""
Intended for main file utilizing a langgraph agent.
"""
import os
import json
from typing import Annotated, Dict, List
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import ToolMessage


print(f"ANTHROPIC_API_KEY: {os.environ.get('ANTHROPIC_API_KEY')}")
print(f"TAVILY_API_KEY:    {os.environ.get('TAVILY_API_KEY')}")


class State(TypedDict):
    """
    State type for the agent.
    """

    messages: Annotated[list, add_messages]

tool = TavilySearchResults(max_results=3)
tools = [tool]

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State) -> Dict:
    return {"messages": [llm.invoke(state["messages"])]}


class BasicToolNode:
    """
    A node that runs the tools requested in the last AIMessage
    """
    def __init__(self, tools: List) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: Dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

tool_node = BasicToolNode(tools=tools)











if __name__ == "__main__":
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tool_node", tool_node)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile()

    def stream_graph_updates(user_input: str):
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]}
        ):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input)
        except:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break
