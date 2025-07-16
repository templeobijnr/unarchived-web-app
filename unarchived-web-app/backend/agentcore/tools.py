from langchain_core.tools import tool
from langchain_openai import ChatOpenAI  # Updated per deprecation warning
from decouple import config
import re
import json

@tool
def file_parser_tool(file_content: str) -> dict:
    """
    Extract basic structured fields from raw file content (e.g., OCR text).
    """
    data = {}

    # Size
    size_match = re.search(r'\b(XL|L|M|S|XS|XXL|[0-9]{2}["\'])\b', file_content)
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
    Extract structured Digital Product Genome (DPG) fields from a natural language prompt + image OCR.
    """
    llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    )

    system_prompt = """
You are a world-class product development analyst and manufacturing sourcing expert.

You help brands convert unstructured product information—whether from text, screenshots, images, PDFs, WhatsApp messages, or design notes—into a clean, structured specification called the Digital Product Genome (DPG).

Extract all relevant sourcing/manufacturing information and output it as a valid JSON with this structure:

{
  "product_title": "string",
  "brand": "string",
  "style_number": "string or null",
  "category": "string",
  "description": "string",
  "materials": ["string"],
  "colors": ["string"],
  "sizes": ["string"],
  "fit": "string",
  "components": {
    "hardware": ["string"],
    "electronics": ["string"],
    "labels": ["string"]
  },
  "features": ["string"],
  "construction_notes": ["string"],
  "packaging": "string or null",
  "compliance_notes": ["string"],
  "image_references": ["string"],
  "extracted_from": ["image", "chat", "pdf", "prompt", "text", "screenshot"],
  "confidence_notes": "string"
}

Respond ONLY with the JSON object and nothing else.
"""

    full_prompt = f"{system_prompt}\n\nInput:\n{prompt}"
    response = llm.invoke(full_prompt)

   # Try to extract JSON from triple backtick block
    match = re.search(r"```json\s*(.*?)```", response.content, re.DOTALL)
    try:
        parsed = json.loads(match.group(1).strip()) if match else json.loads(response.content)
    except json.JSONDecodeError:
        parsed = {}
    return {
        "title": parsed.get("product_title", "Parsed DPG"),
        "version": "1.0",
        "data": {
            "summary": prompt,
            **parsed
        },
        "stage": "created"
    }


@tool
def rfq_generator_tool(dpg_data: dict) -> dict:
    """
    Generate a basic RFQ (Request for Quote) from a DPG.
    """
    return {
        "title": f"RFQ for {dpg_data.get('title', 'Unnamed')}",
        "category": dpg_data.get("data", {}).get("category", "Uncategorized"),
        "status": "draft"
    }
