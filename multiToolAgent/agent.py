from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")


class AgentState(TypedDict):
    messages: list


def call_llm(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


graph = StateGraph(AgentState)
graph.add_node("call_llm", call_llm)
graph.set_entry_point("call_llm")
graph.add_edge("call_llm", END)

app = graph.compile()

result = app.invoke({"messages": [HumanMessage(content="What is 5 + 5?")]})
print(result)