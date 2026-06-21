from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_tavily import TavilySearch




load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

search_tool = TavilySearch(max_results = 3)


class AgentState(TypedDict):
    messages: list # it is just being used for defining the data type which is list here 
                                  

@tool #a python function which will be acting as the tool
def add(a: int,b:int) -> int:
    """adds two numbers together.""" #the llm reads this and then understands ok i have to use this and is sent to the model 
    return a + b

#same here a tool which is nothing but a python function as it makes it discoverable by the langchain tool calling system and its discovering
@tool
def multiply(a: int , b:int) -> int:
    """multiples two numbers together """
    return a*b

# a lookup disctionary for the LLM
# list of all tools the agent can use
tools = [add, multiply, search_tool]

tools_by_name = {t.name: t for t in tools}

llm_with_tools = llm.bind_tools(tools)#telling the llm that these tools exist 


#for every tool requested , it looks up the functions and then parses the values and wrapps it into tool_messages along with the id 

def call_tool(state: AgentState):
    last_message = state["messages"][-1]
    tool_messages = [] #used for wrapping the llm response
    for tool_call in last_message.tool_calls:
      tool_fn = tools_by_name[tool_call["name"]]
      result = tool_fn.invoke(tool_call["args"])
      tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

    return {"messages": state["messages"] + tool_messages}


#a decision for checking whether the llm asked for a tool or actually gave a real answer 
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "call_tool"
    return END


#takes current convo , send it to llm , get one new message bcak a normal answer of a request to use tools , append it to the conversation return the updated state 

def call_llm(state: AgentState): #updating the callllm function to use all the tools allowed 
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}



#registers two nodes , runs call llm first and checks with should continue to decide to go or to stop then call tool run , after getting a solution it will go back to call llm to get the anwer back or a new input that the llm wants to parse through the llm 
graph = StateGraph(AgentState)
graph.add_node("call_llm", call_llm)
graph.add_node("call_tool", call_tool)

graph.set_entry_point("call_llm")

graph.add_conditional_edges("call_llm", should_continue)
graph.add_edge("call_tool", "call_llm") #edge for call tool as they are connected

app = graph.compile()
# for drawing the graph
graph_png = app.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_png)


#actualy execution for the messages d/b human and ai messages
result = app.invoke({"messages": [HumanMessage(content="What is 25 + 35?, and who is the prime minister of india ?")]})
print(result) 

#the llm never runs code , it takes values and gives them to the function and takes the input from that then process it 

#there is a tool execution node too for obv executing a node with the llms input into the function 