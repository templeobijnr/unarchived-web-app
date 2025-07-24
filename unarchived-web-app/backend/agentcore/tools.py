from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
 # Updated per deprecation warning
from decouple import config
import re
import json
from PIL import Image
from io import BytesIO
import pytesseract
import fitz  # PyMuPDF
import docx
import csv
import pandas as pd
import base64


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
            
            **parsed
        },
        "stage": "created"
    }


@tool
def rfq_generator_tool(dpg_data: dict) -> dict:
    """
    Generate a professional RFQ (Request for Quote) from a DPG.
    """
    llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    )
    
    system_prompt = """You are an intelligent procurement assistant.
Based on the provided Digital Product Genome (DPG) data, generate a professional Request for Quote (RFQ) document suitable for sending to suppliers or vendors.

Create a well-structured RFQ document with the following sections:

1. INTRODUCTION
   - Brief explanation of the RFQ purpose
   - Company information (if available)

2. PRODUCT SPECIFICATIONS
   - Extract and format all relevant product details from the DPG
   - Include materials, dimensions, colors, sizes, features, etc.

3. QUANTITY REQUIREMENTS
   - Default to "To be discussed" if not specified

4. TECHNICAL REQUIREMENTS
   - Construction notes
   - Compliance requirements
   - Quality standards

5. SUBMISSION REQUIREMENTS
   - Response deadline
   - Required information from vendors
   - Contact details

6. TERMS & CONDITIONS
   - Delivery expectations
   - Payment terms (standard)

Format the output as a professional document that vendors can easily understand and respond to.
Respond with a complete RFQ document, not just JSON."""

    # Extract DPG data safely
    data = dpg_data.get("data", {}) if isinstance(dpg_data, dict) else {}
    
    # Format the DPG data for the prompt
    dpg_summary = f"""
DIGITAL PRODUCT GENOME DATA:

Product Title: {data.get('product_title', 'Not specified')}
Brand: {data.get('brand', 'Not specified')}
Style Number: {data.get('style_number', 'Not specified')}
Category: {data.get('category', 'Not specified')}
Description: {data.get('description', 'Not specified')}

Materials: {', '.join(data.get('materials', [])) if data.get('materials') else 'Not specified'}
Colors: {', '.join(data.get('colors', [])) if data.get('colors') else 'Not specified'}
Sizes: {', '.join(data.get('sizes', [])) if data.get('sizes') else 'Not specified'}
Fit: {data.get('fit', 'Not specified')}

Components:
- Hardware: {', '.join(data.get('components', {}).get('hardware', [])) if data.get('components', {}).get('hardware') else 'None specified'}
- Electronics: {', '.join(data.get('components', {}).get('electronics', [])) if data.get('components', {}).get('electronics') else 'None specified'}
- Labels: {', '.join(data.get('components', {}).get('labels', [])) if data.get('components', {}).get('labels') else 'None specified'}

Features: {', '.join(data.get('features', [])) if data.get('features') else 'Not specified'}
Construction Notes: {', '.join(data.get('construction_notes', [])) if data.get('construction_notes') else 'Not specified'}
Packaging: {data.get('packaging', 'Not specified')}
Compliance Notes: {', '.join(data.get('compliance_notes', [])) if data.get('compliance_notes') else 'Not specified'}
"""

    full_prompt = f"{system_prompt}\n\n{dpg_summary}"
    
    try:
        response = llm.invoke(full_prompt)
        rfq_content = response.content
        
        return {
            "title": f"RFQ for {data.get('product_title', 'Product')}",
            "category": data.get("category", "Uncategorized"),
            "status": "draft",
            "content": rfq_content,
            "product_title": data.get('product_title', 'Not specified'),
            "brand": data.get('brand', 'Not specified'),
            "generated_from_dpg": dpg_data.get('title', 'Unknown DPG')
        }
    except Exception as e:
        return {
            "title": f"RFQ for {data.get('product_title', 'Product')}",
            "category": data.get("category", "Uncategorized"),
            "status": "error",
            "content": f"Error generating RFQ: {str(e)}",
            "error": str(e)
        }

@tool
def file_parser_tool_base64(content: str, filename: str, content_type: str) -> dict:
    """
    Accepts a base64-encoded file, decodes it, and extracts text depending on the file type.
    Supports: .png, .jpg, .jpeg, .pdf, .docx, .txt, .csv, .xls, .xlsx
    """
    extracted_text = ""

    try:
        # Decode base64 into raw bytes
        file_bytes = base64.b64decode(content)
        filename = filename.lower()

        if content_type.startswith("image/"):
            image = Image.open(BytesIO(file_bytes))
            extracted_text = pytesseract.image_to_string(image)

        elif filename.endswith(".pdf"):
            pdf = fitz.open(stream=file_bytes, filetype="pdf")
            for page in pdf:
                extracted_text += page.get_text()

        elif filename.endswith(".docx"):
            doc = docx.Document(BytesIO(file_bytes))
            extracted_text = "\n".join([para.text for para in doc.paragraphs])

        elif filename.endswith(".txt"):
            extracted_text = file_bytes.decode("utf-8")

        elif filename.endswith(".csv"):
            text = file_bytes.decode("utf-8")
            reader = csv.reader(text.splitlines())
            extracted_text = "\n".join(["\t".join(row) for row in reader])

        elif filename.endswith(".xls") or filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(file_bytes))
            extracted_text = df.to_string(index=False)

        else:
            extracted_text = "Unsupported file format."

    except Exception as e:
        extracted_text = f"Error parsing file: {str(e)}"

    return {"extracted_text": extracted_text.strip()}

from langchain_core.tools import tool
import base64
import json
from io import BytesIO

"""@tool
    def file_parser_tool_base64(encoded_file_str: str) -> dict:
        
        #Accepts a base64-encoded file input (JSON string with 'content', 'filename', 'content_type').
        #Decodes and passes to file_parser_tool().
        
    
        try:
            from agentcore.tools import file_parser_tool
            payload = json.loads(encoded_file_str)
            file_bytes = base64.b64decode(payload["content"])
            filename = payload["filename"]
            content_type = payload["content_type"]
            return file_parser_tool(file_bytes, filename, content_type)
        except Exception as e:
            return {"error": f"Failed to decode or parse: {str(e)}"}"""



@tool
def dpg_summary_tool(dpg_json: dict) -> str:
    """
    Generates a short summary for product managers from a DPG JSON.
    """
    llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    )

    prompt = f"""Summarize this product in 3-4 sentences:\n{json.dumps(dpg_json, indent=2)}"""
    response = llm.invoke(prompt)
    return response.content.strip()
