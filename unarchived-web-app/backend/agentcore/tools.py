
from langchain_core.tools import tool
import json
from decouple import config
from langchain_community.chat_models import ChatOpenAI

@tool
def file_parser_tool(file_content: str) -> dict:
    """
    Extract structured fields from raw file content (e.g., OCR text).
    """
    import re

    data = {}

    # Size
    size_match = re.search(r'\b(XL|L|M|S|XS|XXL|[0-9]{2}[\"\'])\b', file_content)
    if size_match:
        data['size'] = size_match.group(0)

    # Material
    materials = ['cotton', 'canvas', 'polyester', 'nylon', 'leather']
    data['materials'] = [mat for mat in materials if mat in file_content.lower()]

    # Features
    if 'laptop' in file_content.lower():
        data['features'] = ['laptop sleeve']

    return {
        "extracted_text": file_content[:250],
        "structured_data": data,
        "summary": "Auto-extracted basic attributes from spec image"
    }

@tool
def dpg_builder_tool(prompt: str) -> dict:
    """
    Use LLM to extract product title and build DPG from a natural language prompt.
    """
    llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    )
    title_prompt = f"Extract a clean product title from this request: '{prompt}'"

    response = llm.invoke(title_prompt)

    
    return {
        "title": response.content.strip(),
        "version": "1.0",
        "data": {"summary": prompt},
        "stage": "created"
    }

@tool
def rfq_generator_tool(dpg_data: dict) -> dict:
    """
    Generate a request-for-quote from an approved DPG.
    """
    return {
        "title": f"RFQ for {dpg_data.get('title', 'Unnamed')}",
        "category": dpg_data.get("data", {}).get("category", "Uncategorized"),
        "status": "draft"
    }
