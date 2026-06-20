from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")


class AgentState(TypedDict):
    messages: list


@tool
def add(a: int,b:int) -> int:
    """adds two numbers together.""" #the llm reads this and then understands ok i have to use this and is sent to the model 
    return a + b

@tool
def multiply(a: int , b:int) -> int:
    """multiples two numbers together """
    return a*b


tools_by_name = {"add": add,"multiply":multiply}

llm_with_tools = llm.bind_tools([add, multiply])#telling the llm that these tools exist 

def call_tool(state: AgentState):
    last_message = state["messages"][-1]
    tool_messages = []
    for tool_call in last_message.tool_calls:
      tool_fn = tools_by_name[tool_call["name"]]
      result = tool_fn.invoke(tool_call["args"])
      tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

    return {"messages": state["messages"] + [tool_messages]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "call_tool"
    return END

def call_llm(state: AgentState): #updating the callllm function to use all the tools allowed 
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


graph = StateGraph(AgentState)
graph.add_node("call_llm", call_llm)
graph.add_node("call_tool", call_tool)

graph.set_entry_point("call_llm")

graph.add_conditional_edges("call_llm", should_continue)
graph.add_edge("call_tool", "call_llm")

app = graph.compile()

result = app.invoke({"messages": [HumanMessage(content="What is 25 + 35?, and what is 7 times 8?")]})
print(result)

#the llm never runs code , it takes values and gives them to the function and takes the input from that then process it 

#there is a tool execution node too for obv executing a node with the llms input into the function 