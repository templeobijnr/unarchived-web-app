from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from decouple import config

from langchain.agents import Tool
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory  


from .tools import file_parser_tool, dpg_builder_tool, rfq_generator_tool
from dpgs.models import DigitalProductGenome
import os

def get_memory(session_id):
    redis_url = config("REDIS_URL", default="redis://localhost:6379")
    history = RedisChatMessageHistory(session_id=session_id, url=redis_url)
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, chat_memory=history
    )
    return memory

def create_co_pilot_agent(session_id, user):
    llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    )
    def create_dpg_tool(parsed_text: str) -> str:
        dpg = DigitalProductGenome.objects.create(
            title="Auto-generated DPG",
            description="Generated from AI chat",
            owner=user,
            data={"raw_text": parsed_text},
            stage="created"
        )
        return f"DPG created with ID {dpg.id} and title '{dpg.title}'"

    tools = [
        file_parser_tool,
        dpg_builder_tool,
        rfq_generator_tool,
        Tool.from_function(name="create_dpg_tool", func=create_dpg_tool, description="Create a DPG from parsed file text")
    ]

    memory = get_memory(session_id)
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        verbose=True,
        memory=memory
    )