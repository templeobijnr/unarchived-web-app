
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
from langchain.agents.agent_toolkits import Tool
from .tools import file_parser_tool, dpg_builder_tool, rfq_generator_tool
import os

def get_memory(session_id):
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    history = RedisChatMessageHistory(session_id=session_id, url=redis_url)
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, chat_memory=history
    )
    return memory

def create_co_pilot_agent(session_id):
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    tools = [file_parser_tool, dpg_builder_tool, rfq_generator_tool]
    memory = get_memory(session_id)

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        verbose=True,
        memory=memory
    )
