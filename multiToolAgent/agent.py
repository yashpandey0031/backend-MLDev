from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")


class AgentState(TypedDict):
    messages: list


@tool
def add(a: int,b:int) -> int:
    """adds two numbers together.""" #the llm reads this and then understands ok i have to use this and is sent to the model 
    return a + b

llm_with_tools = llm.bind_tools([add]) #telling the llm that these tools exist 

def call_llm(state: AgentState): #updating the callllm function to use all the tools allowed 
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


graph = StateGraph(AgentState)
graph.add_node("call_llm", call_llm)
graph.set_entry_point("call_llm")
graph.add_edge("call_llm", END)

app = graph.compile()

result = app.invoke({"messages": [HumanMessage(content="What is 25 + 35?")]})
print(result)