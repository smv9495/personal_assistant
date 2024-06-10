from setup_env import load_env

# Chat Model
from langchain_google_genai import ChatGoogleGenerativeAI

# Prompt related imports
from langchain_core.prompts import (ChatMessagePromptTemplate, 
                                    HumanMessagePromptTemplate, 
                                    AIMessagePromptTemplate, 
                                    SystemMessagePromptTemplate)

from calendar_agent import view_events_tool


# load API Keys
load_env()

# create llm object
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

tools = [view_events_tool]
llm_with_tools = llm.bind_tools(tools)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very my personal assistant.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=[view_events_tool], verbose=True)

list(agent_executor.stream({"input":"Hi, how are you?"}))
