from langchain_core.tools import tool



@tool
def file_parser_tool(file_content: str) -> dict:
    '''Parse raw file content into structured components.'''
    # Simulate logic – in reality, you'd use OCR or pattern matching
    return {"extracted_text": file_content[:100], "summary": "Sample parsed structure"}

@tool
def dpg_builder_tool(parsed_data: dict) -> dict:
    '''Build a Digital Product Genome (DPG) from structured input.'''
    return {
        "title": parsed_data.get("summary", "Untitled Product"),
        "version": "1.0",
        "data": parsed_data,
        "stage": "created"
    }

@tool
def rfq_generator_tool(dpg_data: dict) -> dict:
    '''Generate a request-for-quote from an approved DPG.'''
    return {
        "title": f"RFQ for {dpg_data.get('title', 'Unnamed')}",
        "category": dpg_data.get("data", {}).get("category", "Uncategorized"),
        "status": "draft"
    }