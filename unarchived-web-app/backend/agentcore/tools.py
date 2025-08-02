from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage
from langchain_community.tools import TavilySearchResults
from langchain_openai import OpenAIEmbeddings
from pgvector.django import L2Distance
from decouple import config
from pydantic import BaseModel
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
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from knowledge_base.models import KnowledgeChunk

# Configure logging
logger = logging.getLogger(__name__)

# Initialize LLM instances
llm = ChatOpenAI(
    model_name=config("OPENAI_MODEL", default="gpt-4"),
    openai_api_key=config("OPENAI_API_KEY"),
    temperature=0
)

# Enhanced DPG Schema for structured output (as recommended in Phase 3)
class DPGSchema(BaseModel):
    product_title: str | None = None
    brand: str | None = None
    style_number: str | None = None
    category: str | None = None
    description: str | None = None
    materials: List[Dict[str, str]] | None = None  # Enhanced to include component mapping
    colors: List[str] | None = None
    sizes: List[str] | None = None
    fit: str | None = None
    dimensions: Dict[str, str] | None = None  # Added dimensions
    weight: str | None = None  # Added weight
    components: Dict[str, List[str]] | None = None
    features: List[str] | None = None
    construction_notes: List[str] | None = None
    manufacturing_process: List[str] | None = None  # Added manufacturing details
    sustainability_notes: List[str] | None = None  # Added sustainability
    compliance_requirements: List[str] | None = None  # Enhanced compliance
    packaging: str | None = None
    target_price_range: str | None = None  # Added pricing
    moq_requirements: str | None = None  # Added MOQ
    lead_time_expectations: str | None = None  # Added timing
    image_references: List[str] | None = None
    extracted_from: List[str] | None = None
    confidence_notes: str | None = None


def knowledge_base_retriever_tool(query: str) -> str:
    """Retrieve relevant knowledge chunks from the Knowledge Base."""
    knowledge = KnowledgeChunk.objects.filter(content__icontains=query)
    return "\n".join([chunk.content for chunk in knowledge])

@tool
def dpg_builder_tool(prompt: str) -> dict:
    """
    Enhanced DPG builder with structured output and expert knowledge integration.
    Creates a comprehensive Digital Product Genome from natural language input.
    """
    # Use structured output to ensure consistent JSON format
    structured_llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0.1
    ).with_structured_output(DPGSchema)

    system_prompt = """You are a world-class product development analyst and manufacturing sourcing expert with deep knowledge of materials, processes, and compliance requirements.

Convert the provided product information into a comprehensive Digital Product Genome (DPG). Use your expertise to:

1. IDENTIFY KEY SPECIFICATIONS:
   - Extract explicit product details
   - Infer missing but critical information based on product category
   - Suggest industry-standard materials and processes where appropriate

2. ENHANCE WITH EXPERT KNOWLEDGE:
   - Add relevant compliance requirements based on product category and target markets
   - Suggest appropriate manufacturing processes
   - Include sustainability considerations
   - Estimate realistic MOQ and lead time expectations

3. STRUCTURE COMPREHENSIVELY:
   - Organize materials by component (e.g., body, lining, hardware)
   - Include dimensional specifications where relevant
   - Add construction and manufacturing notes
   - Specify quality and testing requirements

4. MAINTAIN ACCURACY:
   - Only include information that can be reasonably inferred
   - Mark uncertain details in confidence_notes
   - Use industry-standard terminology

Extract and structure all relevant information while maintaining accuracy and completeness."""

    try:
        response = structured_llm.invoke(f"{system_prompt}\n\nProduct Information:\n{prompt}")
        dpg_data = response.dict()
        
        return {
            "title": dpg_data.get("product_title", "New Product Specification"),
            "version": "1.0",
            "data": dpg_data,
            "stage": "created"
        }
    except Exception as e:
        logger.error(f"DPG builder error: {str(e)}")
        # Fallback to original implementation
        return _fallback_dpg_builder(prompt)

def _fallback_dpg_builder(prompt: str) -> dict:
    """Fallback DPG builder for when structured output fails."""
    response = llm.invoke(f"""
You are a product development expert. Extract structured product information from this input and return ONLY a valid JSON object:

{prompt}

Return JSON with this structure:
{{
  "product_title": "string",
  "category": "string",
  "description": "string",
  "materials": ["string"],
  "colors": ["string"],
  "features": ["string"]
}}
""")
    
    try:
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            parsed = {"product_title": "Parsed Product", "description": prompt[:200]}
        
        return {
            "title": parsed.get("product_title", "New Product"),
            "version": "1.0",
            "data": parsed,
            "stage": "created"
        }
    except json.JSONDecodeError:
        return {
            "title": "New Product",
            "version": "1.0", 
            "data": {"product_title": "New Product", "description": prompt[:200]},
            "stage": "created"
        }

@tool
def dpg_updater_tool(current_dpg_json: dict, new_information_prompt: str) -> dict:
    """
    Enhanced DPG updater that intelligently merges new information with existing DPG.
    Implements the 'living DPG' concept from Phase 3 of the specifications.
    """
    structured_llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    ).with_structured_output(DPGSchema)

    # Extract current data safely
    current_data = current_dpg_json.get("data", {}) if isinstance(current_dpg_json, dict) else current_dpg_json

    prompt = f"""You are a product specification expert. Update this existing Digital Product Genome (DPG) with new information.

CURRENT DPG DATA:
{json.dumps(current_data, indent=2)}

NEW INFORMATION TO INTEGRATE:
{new_information_prompt}

INTEGRATION RULES:
1. If a field exists, intelligently merge or update it (don't just overwrite)
2. For lists (materials, features, etc.), append new items without duplicating
3. For materials, map to specific components when possible
4. Add new fields as appropriate
5. Preserve existing structure and valuable data
6. Enhance specifications with expert knowledge when new info suggests it
7. Update confidence_notes to reflect changes made

Be thorough and maintain data integrity while incorporating all relevant new information."""

    try:
        response = structured_llm.invoke(prompt)
        updated_data = response.dict()
        
        # Remove None values to keep JSON clean
        updated_data = {k: v for k, v in updated_data.items() if v is not None}
        
        return {
            "title": updated_data.get("product_title", current_dpg_json.get("title", "Updated Product")),
            "version": "1.1",
            "data": updated_data,
            "stage": "updated"
        }
        
    except Exception as e:
        logger.error(f"DPG update failed: {str(e)}")
        return current_dpg_json

@tool
def knowledge_base_retriever_tool(query: str, domain: Optional[str] = None, limit: int = 5) -> str:
    """
    Searches the Unarchived expert knowledge base for information on materials,
    processes, and compliance to answer specific user questions.
    
    Args:
        query: The search query string
        domain: Optional domain filter (e.g., 'materials', 'manufacturing', 'compliance')
        limit: Maximum number of chunks to retrieve (default: 5)
    
    Returns:
        Formatted context string with relevant expert knowledge
    """
    try:
        # Initialize embeddings model
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=config("OPENAI_API_KEY")
        )
        
        # Generate query embedding
        query_embedding = embeddings_model.embed_query(query)
        
        # Build the base queryset
        queryset = KnowledgeChunk.objects.all()
        
        # Apply domain filter if specified
        if domain:
            queryset = queryset.filter(domain__icontains=domain)
        
        # Perform similarity search using L2Distance
        # Order by similarity (smallest distance = most similar)
        closest_chunks = queryset.annotate(
            similarity=L2Distance('embedding', query_embedding)
        ).order_by('similarity')[:limit]
        
        if not closest_chunks.exists():
            return f"I could not find any specific information about '{query}' in my knowledge base. Please try a different query or provide more context."
        
        # Format the results
        context = "--- Expert Knowledge Base Context ---\n\n"
        
        for i, chunk in enumerate(closest_chunks, 1):
            # Build source information
            source_info = f"{chunk.source_document}"
            if chunk.entity_name:
                source_info += f" ({chunk.entity_name})"
            
            # Add domain/subdomain context
            domain_info = chunk.domain.title()
            if chunk.subdomain:
                domain_info += f" > {chunk.subdomain.title()}"
            
            # Format each chunk
            context += f"Result {i} - {domain_info}\n"
            context += f"Source: {source_info}\n"
            if chunk.confidence_score < 1.0:
                context += f"Confidence: {chunk.confidence_score:.2f}\n"
            context += f"Content: {chunk.content}\n"
            
            # Add metadata if available and relevant
            if chunk.metadata:
                relevant_metadata = []
                for key, value in chunk.metadata.items():
                    if key in ['material_type', 'process_type', 'compliance_region', 'supplier_type']:
                        relevant_metadata.append(f"{key.replace('_', ' ').title()}: {value}")
                
                if relevant_metadata:
                    context += f"Additional Info: {', '.join(relevant_metadata)}\n"
            
            context += "\n" + "-" * 50 + "\n\n"
        
        # Add search metadata
        context += f"Search performed for: '{query}'\n"
        if domain:
            context += f"Filtered by domain: '{domain}'\n"
        context += f"Results returned: {len(closest_chunks)} of {KnowledgeChunk.objects.count()} total chunks\n"
        
        return context
        
    except Exception as e:
        logger.error(f"Knowledge base retrieval error: {str(e)}")
        return f"I encountered an error searching the knowledge base for '{query}': {str(e)}. Please try a more specific query or contact support."

@tool
def knowledge_base_domain_search_tool(query: str, domain: str, subdomain: Optional[str] = None) -> str:
    """
    Searches the knowledge base with specific domain filtering for more targeted results.
    
    Args:
        query: The search query string
        domain: Specific domain to search in (e.g., 'materials', 'manufacturing', 'compliance')
        subdomain: Optional subdomain filter for more specific results
    
    Returns:
        Formatted context string with domain-specific expert knowledge
    """
    try:
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=config("OPENAI_API_KEY")
        )
        
        query_embedding = embeddings_model.embed_query(query)
        
        # Build filtered queryset
        queryset = KnowledgeChunk.objects.filter(domain__iexact=domain)
        
        if subdomain:
            queryset = queryset.filter(subdomain__icontains=subdomain)
        
        # Perform similarity search
        closest_chunks = queryset.annotate(
            similarity=L2Distance('embedding', query_embedding)
        ).order_by('similarity')[:5]
        
        if not closest_chunks.exists():
            available_domains = KnowledgeChunk.objects.values_list('domain', flat=True).distinct()
            return f"No results found in domain '{domain}'{f' > {subdomain}' if subdomain else ''}. Available domains: {', '.join(available_domains)}"
        
        # Format results with domain-specific context
        context = f"--- {domain.title()} Domain Expert Knowledge ---\n\n"
        
        for chunk in closest_chunks:
            context += f"Entity: {chunk.entity_name or 'General'}\n"
            context += f"Source: {chunk.source_document}\n"
            context += f"Content: {chunk.content}\n\n"
            
            if chunk.metadata:
                context += f"Technical Details: {chunk.metadata}\n"
            
            context += "-" * 40 + "\n\n"
        
        return context
        
    except Exception as e:
        logger.error(f"Domain search error: {str(e)}")
        return f"Error searching {domain} domain: {str(e)}"

@tool
def knowledge_base_entity_search_tool(entity_name: str) -> str:
    """
    Searches for all information about a specific entity (material, process, supplier, etc.).
    
    Args:
        entity_name: Name of the entity to search for
        
    Returns:
        Comprehensive information about the specified entity
    """
    try:
        # Search for exact and partial matches
        exact_matches = KnowledgeChunk.objects.filter(entity_name__iexact=entity_name)
        partial_matches = KnowledgeChunk.objects.filter(
            entity_name__icontains=entity_name
        ).exclude(entity_name__iexact=entity_name)
        
        if not exact_matches.exists() and not partial_matches.exists():
            return f"No information found for entity '{entity_name}'. Try searching with a more general term."
        
        context = f"--- Complete Entity Profile: {entity_name} ---\n\n"
        
        # Process exact matches first
        if exact_matches.exists():
            context += "EXACT MATCHES:\n"
            for chunk in exact_matches.order_by('domain', 'subdomain'):
                context += f"\nDomain: {chunk.domain} > {chunk.subdomain or 'General'}\n"
                context += f"Source: {chunk.source_document}\n"
                context += f"Content: {chunk.content}\n"
                
                if chunk.metadata:
                    context += f"Specifications: {chunk.metadata}\n"
                context += "\n"
        
        # Process partial matches
        if partial_matches.exists():
            context += "\nRELATED ENTITIES:\n"
            for chunk in partial_matches.order_by('entity_name')[:3]:  # Limit related results
                context += f"\n{chunk.entity_name} ({chunk.domain})\n"
                context += f"Content: {chunk.content[:200]}...\n"
        
        return context
        
    except Exception as e:
        logger.error(f"Entity search error: {str(e)}")
        return f"Error searching for entity '{entity_name}': {str(e)}"

@tool
def knowledge_base_stats_tool() -> str:
    """
    Provides statistics about the knowledge base content for system monitoring.
    
    Returns:
        Summary statistics about the knowledge base
    """
    try:
        from django.db.models import Count, Avg
        
        total_chunks = KnowledgeChunk.objects.count()
        
        if total_chunks == 0:
            return "Knowledge base is empty. Please run the ingestion pipeline to populate it."
        
        # Domain distribution
        domain_stats = KnowledgeChunk.objects.values('domain').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Source distribution
        source_stats = KnowledgeChunk.objects.values('source_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Average confidence score
        avg_confidence = KnowledgeChunk.objects.aggregate(
            avg_confidence=Avg('confidence_score')
        )['avg_confidence']
        
        stats = f"--- Knowledge Base Statistics ---\n\n"
        stats += f"Total Knowledge Chunks: {total_chunks:,}\n"
        stats += f"Average Confidence Score: {avg_confidence:.3f}\n\n"
        
        stats += "DOMAIN DISTRIBUTION:\n"
        for domain_stat in domain_stats:
            percentage = (domain_stat['count'] / total_chunks) * 100
            stats += f"  {domain_stat['domain'].title()}: {domain_stat['count']} ({percentage:.1f}%)\n"
        
        stats += "\nSOURCE TYPE DISTRIBUTION:\n"
        for source_stat in source_stats:
            percentage = (source_stat['count'] / total_chunks) * 100
            stats += f"  {source_stat['source_type'].replace('_', ' ').title()}: {source_stat['count']} ({percentage:.1f}%)\n"
        
        # Recent additions
        recent_chunks = KnowledgeChunk.objects.order_by('-created_at')[:5]
        if recent_chunks:
            stats += "\nRECENT ADDITIONS:\n"
            for chunk in recent_chunks:
                stats += f"  {chunk.entity_name or 'General'} ({chunk.domain}) - {chunk.created_at.strftime('%Y-%m-%d')}\n"
        
        return stats
        
    except Exception as e:
        logger.error(f"Knowledge base stats error: {str(e)}")
        return f"Error retrieving knowledge base statistics: {str(e)}"

# Update the original tool to use the enhanced version
knowledge_base_retriever_tool = knowledge_base_retriever_tool
@tool
def web_search_tool(query: str) -> str:
    """
    Enhanced web search tool for finding current supplier information, pricing, and market data.
    Implements the live data access recommended in Phase 4.
    """
    try:
        # Initialize Tavily search (you'll need to install: pip install tavily-python)
        search = TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_domains=["alibaba.com", "made-in-china.com", "thomasnet.com", "globalspec.com"]
        )
        
        results = search.invoke(query)
        
        if not results:
            return f"No current web results found for '{query}'. Please try a different search term."
        
        # Format results for better readability
        formatted_results = f"--- Current Web Search Results for '{query}' ---\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            content = result.get('content', 'No content')
            url = result.get('url', 'No URL')
            
            formatted_results += f"{i}. {title}\n"
            formatted_results += f"   {content[:200]}...\n"
            formatted_results += f"   Source: {url}\n\n"
        
        return formatted_results
        
    except ImportError:
        logger.warning("Tavily search not available. Install with: pip install tavily-python")
        return f"Web search capability not configured. Please install required dependencies for live supplier search."
    except Exception as e:
        logger.error(f"Web search error: {str(e)}")
        return f"Error performing web search for '{query}': {str(e)}"

@tool
def image_analyzer_tool(image_base64: str, analysis_prompt: str) -> str:
    """
    Analyzes product images using GPT-4 Vision to identify components, materials, and construction details.
    Enhanced implementation from Phase 4 specifications.
    """
    try:
        llm_vision = ChatOpenAI(
            model="gpt-4-vision-preview", 
            max_tokens=1024,
            temperature=0
        )
        
        # Enhanced prompt for product development context
        enhanced_prompt = f"""You are a product development expert analyzing this image. 

{analysis_prompt}

Please provide detailed observations about:
1. Materials used (fabric, hardware, etc.)
2. Construction methods and techniques
3. Design features and functionality
4. Quality indicators
5. Manufacturing considerations
6. Any visible brand/style details

Focus on technical details that would be useful for product specifications or manufacturing."""

        message = HumanMessage(
            content=[
                {"type": "text", "text": enhanced_prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                }
            ]
        )
        
        response = llm_vision.invoke([message])
        return response.content
        
    except Exception as e:
        logger.error(f"Image analysis error: {str(e)}")
        return f"Error analyzing image: {str(e)}. Please ensure the image is properly formatted and try again."

@tool
def supplier_discovery_tool(product_category: str, location_preference: str = "global") -> str:
    """
    Discovers potential suppliers based on product category and location preferences.
    Combines web search with knowledge base for comprehensive supplier information.
    """
    try:
        # Construct search query for suppliers
        search_query = f"{product_category} manufacturers suppliers {location_preference}"
        
        # Get web search results
        web_results = web_search_tool.func(search_query)
        
        # Get knowledge base context about supplier considerations
        kb_context = knowledge_base_retriever_tool.func(f"supplier selection {product_category}")
        
        # Combine and format results
        supplier_info = f"""--- Supplier Discovery Results ---

CURRENT MARKET SEARCH:
{web_results}

EXPERT GUIDANCE:
{kb_context}

NEXT STEPS:
1. Contact identified suppliers for capability assessment
2. Request samples and technical specifications
3. Conduct facility audits for shortlisted suppliers
4. Negotiate terms and establish partnerships

Note: Always verify supplier credentials, certifications, and references before proceeding."""

        return supplier_info
        
    except Exception as e:
        logger.error(f"Supplier discovery error: {str(e)}")
        return f"Error in supplier discovery: {str(e)}"

@tool
def compliance_checker_tool(product_category: str, target_markets: List[str]) -> str:
    """
    Checks compliance requirements for products in specific markets.
    Uses knowledge base to provide relevant regulatory information.
    """
    try:
        markets_str = ", ".join(target_markets)
        query = f"compliance requirements {product_category} {markets_str} regulations"
        
        compliance_info = knowledge_base_retriever_tool.func(query)
        
        # Enhanced with market-specific considerations
        enhanced_response = f"""--- Compliance Requirements Analysis ---

Product Category: {product_category}
Target Markets: {markets_str}

{compliance_info}

RECOMMENDED ACTIONS:
1. Review all applicable standards and regulations
2. Plan for required testing and certification
3. Budget for compliance costs (typically 2-5% of production cost)
4. Allow additional 4-6 weeks in timeline for testing
5. Establish relationships with accredited testing laboratories

CRITICAL: Always consult with regulatory experts and testing laboratories for definitive compliance guidance."""

        return enhanced_response
        
    except Exception as e:
        logger.error(f"Compliance check error: {str(e)}")
        return f"Error checking compliance requirements: {str(e)}"

@tool
def rfq_generator_tool(dpg_data: dict) -> dict:
    """
    Enhanced RFQ generator with professional formatting and comprehensive specifications.
    Implements recommendations from Phase 4 for better supplier communication.
    """
    try:
        # Extract DPG data safely
        data = dpg_data.get("data", {}) if isinstance(dpg_data, dict) else {}
        
        # Enhanced system prompt for professional RFQ generation
        system_prompt = """You are a professional procurement specialist. Generate a comprehensive, professional Request for Quote (RFQ) document that suppliers can easily understand and respond to accurately.

The RFQ should be detailed, specific, and include all necessary information for suppliers to provide accurate quotes.

Structure the RFQ with these sections:
1. EXECUTIVE SUMMARY
2. PRODUCT SPECIFICATIONS (detailed technical requirements)
3. QUALITY REQUIREMENTS & STANDARDS
4. QUANTITY & DELIVERY REQUIREMENTS
5. SUPPLIER QUALIFICATIONS
6. SUBMISSION REQUIREMENTS
7. EVALUATION CRITERIA
8. TERMS & CONDITIONS

Make it professional, clear, and actionable."""

        # Build comprehensive product information
        product_info = f"""
PRODUCT INFORMATION:
Product Title: {data.get('product_title', 'Not specified')}
Brand: {data.get('brand', 'Not specified')}
Category: {data.get('category', 'Not specified')}
Description: {data.get('description', 'Not specified')}

MATERIALS & SPECIFICATIONS:
Materials: {json.dumps(data.get('materials', []), indent=2) if data.get('materials') else 'Not specified'}
Dimensions: {json.dumps(data.get('dimensions', {}), indent=2) if data.get('dimensions') else 'Not specified'}
Weight: {data.get('weight', 'Not specified')}
Colors: {', '.join(data.get('colors', [])) if data.get('colors') else 'Not specified'}
Sizes: {', '.join(data.get('sizes', [])) if data.get('sizes') else 'Not specified'}

COMPONENTS:
Hardware: {', '.join(data.get('components', {}).get('hardware', [])) if data.get('components', {}).get('hardware') else 'None specified'}
Electronics: {', '.join(data.get('components', {}).get('electronics', [])) if data.get('components', {}).get('electronics') else 'None specified'}
Labels: {', '.join(data.get('components', {}).get('labels', [])) if data.get('components', {}).get('labels') else 'None specified'}

MANUFACTURING:
Construction Notes: {', '.join(data.get('construction_notes', [])) if data.get('construction_notes') else 'Not specified'}
Manufacturing Process: {', '.join(data.get('manufacturing_process', [])) if data.get('manufacturing_process') else 'Not specified'}

BUSINESS REQUIREMENTS:
Target Price Range: {data.get('target_price_range', 'To be discussed')}
MOQ Requirements: {data.get('moq_requirements', 'To be discussed')}
Lead Time Expectations: {data.get('lead_time_expectations', 'To be discussed')}

COMPLIANCE:
Compliance Requirements: {', '.join(data.get('compliance_requirements', [])) if data.get('compliance_requirements') else 'Standard industry requirements'}
Sustainability Notes: {', '.join(data.get('sustainability_notes', [])) if data.get('sustainability_notes') else 'Not specified'}

PACKAGING:
Packaging Requirements: {data.get('packaging', 'Standard protective packaging')}
"""

        full_prompt = f"{system_prompt}\n\n{product_info}"
        
        response = llm.invoke(full_prompt)
        rfq_content = response.content
        
        return {
            "title": f"RFQ - {data.get('product_title', 'Product Specification')}",
            "category": data.get("category", "General"),
            "status": "draft",
            "content": rfq_content,
            "product_title": data.get('product_title', 'Not specified'),
            "brand": data.get('brand', 'Not specified'),
            "generated_from_dpg": dpg_data.get('title', 'Product Specification'),
            "created_date": "Generated via AI Assistant",
            "sections": [
                "Executive Summary",
                "Product Specifications", 
                "Quality Requirements",
                "Quantity & Delivery",
                "Supplier Qualifications",
                "Submission Requirements",
                "Evaluation Criteria",
                "Terms & Conditions"
            ]
        }
        
    except Exception as e:
        logger.error(f"RFQ generation error: {str(e)}")
        return {
            "title": f"RFQ - {data.get('product_title', 'Product')}",
            "status": "error",
            "content": f"Error generating RFQ: {str(e)}",
            "error": str(e)
        }

@tool
def file_parser_tool_base64(content: str, filename: str, content_type: str) -> dict:
    """
    Enhanced file parser with better error handling and content extraction.
    Supports multiple file formats for product development workflows.
    """
    extracted_text = ""
    metadata = {
        "filename": filename,
        "content_type": content_type,
        "file_size": len(content) if content else 0,
        "processing_status": "success"
    }

    try:
        # Decode base64 into raw bytes
        file_bytes = base64.b64decode(content)
        filename_lower = filename.lower()

        if content_type.startswith("image/") or any(filename_lower.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
            try:
                image = Image.open(BytesIO(file_bytes))
                extracted_text = pytesseract.image_to_string(image)
                metadata["image_dimensions"] = f"{image.width}x{image.height}"
                metadata["image_format"] = image.format
            except Exception as e:
                extracted_text = f"Error processing image: {str(e)}"
                metadata["processing_status"] = "error"

        elif filename_lower.endswith(".pdf"):
            try:
                pdf = fitz.open(stream=file_bytes, filetype="pdf")
                text_parts = []
                for page_num, page in enumerate(pdf):
                    page_text = page.get_text()
                    if page_text.strip():
                        text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
                extracted_text = "\n\n".join(text_parts)
                metadata["page_count"] = len(pdf)
                pdf.close()
            except Exception as e:
                extracted_text = f"Error processing PDF: {str(e)}"
                metadata["processing_status"] = "error"

        elif filename_lower.endswith(".docx"):
            try:
                doc = docx.Document(BytesIO(file_bytes))
                paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
                extracted_text = "\n".join(paragraphs)
                metadata["paragraph_count"] = len(paragraphs)
            except Exception as e:
                extracted_text = f"Error processing DOCX: {str(e)}"
                metadata["processing_status"] = "error"

        elif filename_lower.endswith(".txt"):
            try:
                extracted_text = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    extracted_text = file_bytes.decode("latin-1")
                except Exception as e:
                    extracted_text = f"Error decoding text file: {str(e)}"
                    metadata["processing_status"] = "error"

        elif filename_lower.endswith(".csv"):
            try:
                text = file_bytes.decode("utf-8")
                reader = csv.reader(text.splitlines())
                rows = list(reader)
                extracted_text = "\n".join(["\t".join(row) for row in rows])
                metadata["row_count"] = len(rows)
                metadata["column_count"] = len(rows[0]) if rows else 0
            except Exception as e:
                extracted_text = f"Error processing CSV: {str(e)}"
                metadata["processing_status"] = "error"

        elif filename_lower.endswith((".xls", ".xlsx")):
            try:
                df = pd.read_excel(BytesIO(file_bytes))
                extracted_text = df.to_string(index=False)
                metadata["row_count"] = len(df)
                metadata["column_count"] = len(df.columns)
            except Exception as e:
                extracted_text = f"Error processing Excel file: {str(e)}"
                metadata["processing_status"] = "error"

        else:
            extracted_text = "Unsupported file format. Supported formats: PDF, DOCX, TXT, CSV, XLS/XLSX, and common image formats."
            metadata["processing_status"] = "unsupported"

    except Exception as e:
        extracted_text = f"Error parsing file: {str(e)}"
        metadata["processing_status"] = "error"

    # Clean up extracted text
    if extracted_text and metadata["processing_status"] == "success":
        extracted_text = extracted_text.strip()
        metadata["character_count"] = len(extracted_text)
        metadata["word_count"] = len(extracted_text.split()) if extracted_text else 0

    return {
        "extracted_text": extracted_text,
        "metadata": metadata,
        "success": metadata["processing_status"] == "success"
    }

@tool
def dpg_summary_tool(dpg_json: dict) -> str:
    """
    Enhanced DPG summary tool that provides comprehensive product overview.
    """
    try:
        data = dpg_json.get("data", {}) if isinstance(dpg_json, dict) else dpg_json
        
        summary_prompt = f"""Create a comprehensive but concise summary of this product specification for stakeholders:

{json.dumps(data, indent=2)}

Include:
1. Product overview (2-3 sentences)
2. Key specifications and features
3. Manufacturing complexity assessment
4. Market positioning insights
5. Key considerations for production

Keep it professional and actionable for product managers and development teams."""

        response = llm.invoke(summary_prompt)
        return response.content.strip()
        
    except Exception as e:
        logger.error(f"DPG summary error: {str(e)}")
        return f"Error generating summary: {str(e)}"

# Export all tools for easy import
__all__ = [
    'dpg_builder_tool',
    'dpg_updater_tool', 
    'knowledge_base_retriever_tool',
    'web_search_tool',
    'image_analyzer_tool',
    'supplier_discovery_tool',
    'compliance_checker_tool',
    'rfq_generator_tool',
    'file_parser_tool_base64',
    'dpg_summary_tool'
]