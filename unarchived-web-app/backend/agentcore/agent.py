from typing import TypedDict, List, Dict, Any, Literal
from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from decouple import config
import json
import re
import logging
from django.db import transaction
from dpgs.models import DigitalProductGenome
# Import ALL tools from tools.py (updated imports)
from .tools import (
    dpg_builder_tool, 
    dpg_updater_tool,
    rfq_generator_tool, 
    file_parser_tool_base64, 
    dpg_summary_tool,
    knowledge_base_retriever_tool,
    knowledge_base_domain_search_tool,
    knowledge_base_entity_search_tool,
    knowledge_base_stats_tool,
    web_search_tool,
    image_analyzer_tool,
    supplier_discovery_tool,
    compliance_checker_tool,
)

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    model_name=config("OPENAI_MODEL", default="gpt-4"),
    openai_api_key=config("OPENAI_API_KEY"),
    temperature=0.1
)

# Enhanced AgentState following the review recommendations
class AgentState(TypedDict):
    # Core conversation data
    messages: List[Dict[str, Any]]
    
    # Working data (the "living" objects)
    dpg_in_progress: Dict[str, Any]  # The DPG being built/updated
    dpg_id: int | None  # Database ID of current DPG
    
    # Analysis and context
    analysis: Dict[str, Any]  # Output from conversation analyzer
    retrieved_context: str  # Context from knowledge base (when available)
    
    # Control flow tracking
    last_action: Literal[
        "start", "controller", "ask_questions", "knowledge_retrieval", 
        "dpg_update", "rfq_generation", "file_processing", "supplier_discovery",
        "compliance_check", "image_analysis", "web_search", "general_response"
    ] | None
    
    # Session data
    file_outputs: List[Dict[str, Any]]
    conversation_context: Dict[str, Any]
    image_data: str | None  # For image analysis
    search_results: str | None  # For web search results

@tool
def conversation_analyzer_tool(conversation_history: str, current_message: str) -> dict:
    """
    Analyzes the conversation to determine the best next action and what information might be missing.
    This is the 'brain' or 'controller' that the review recommended.
    """
    analysis_llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    )
    
    prompt = f"""You are an expert conversation analyzer for a product development assistant. 
Analyze this conversation and determine the next best action.

CONVERSATION HISTORY:
{conversation_history}

CURRENT MESSAGE:
{current_message}

Based on the conversation, determine:
1. What product information has been gathered?
2. What key information is still missing for a complete DPG?
3. What should be the next action?
4. What specific questions should be asked if more info is needed?

AVAILABLE ACTIONS:
- ask_questions: When more product info is needed
- create_dpg: When enough info exists to create initial DPG
- update_dpg: When updating existing DPG with new info
- create_rfq: When DPG exists and user wants supplier quotes
- process_file: When files need to be processed
- knowledge_retrieval: When user asks about materials, processes, compliance
- supplier_discovery: When user wants to find suppliers
- compliance_check: When user asks about regulations/standards
- image_analysis: When user uploads images for analysis
- web_search: When current market data is needed
- general_response: For general conversation/questions

Respond with JSON:
{{
    "product_info_gathered": {{"title": "...", "materials": [], "features": [], "etc": "..."}},
    "missing_info": ["list of missing key information"],
    "recommended_action": "ask_questions|create_dpg|update_dpg|create_rfq|process_file|knowledge_retrieval|supplier_discovery|compliance_check|image_analysis|web_search|general_response",
    "confidence_level": "high|medium|low",
    "suggested_questions": ["specific questions to ask if action is ask_questions"],
    "reasoning": "brief explanation of recommendation"
}}"""
    
    try:
        response = analysis_llm.invoke(prompt)
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {
                "recommended_action": "general_response",
                "reasoning": "Could not parse analysis response"
            }
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return {
            "recommended_action": "general_response", 
            "reasoning": f"Analysis error: {str(e)}"
        }

# All available tools
tools = [
    file_parser_tool_base64, 
    dpg_builder_tool, 
    dpg_updater_tool,
    rfq_generator_tool, 
    dpg_summary_tool, 
    knowledge_base_retriever_tool,
    knowledge_base_domain_search_tool,
    knowledge_base_entity_search_tool,
    knowledge_base_stats_tool,
    web_search_tool,
    image_analyzer_tool,
    supplier_discovery_tool,
    compliance_checker_tool,
    conversation_analyzer_tool
]

# Node Functions (Enhanced with all tools)

def controller_node(state: AgentState) -> AgentState:
    """
    The 'brain' of the agent. Analyzes conversation and determines next action.
    Enhanced to handle all available tools and capabilities.
    """
    print("---CONTROLLER NODE---")
    
    # Get conversation history as string
    history_str = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in state['messages']
    ])
    current_message = state['messages'][-1]['content'] if state['messages'] else ""
    
    # Analyze the conversation
    analysis = conversation_analyzer_tool.func(history_str, current_message)
    
    # Update state with analysis
    state['analysis'] = analysis
    state['last_action'] = "controller"
    
    logger.info(f"Controller decision: {analysis.get('recommended_action', 'unknown')}")
    return state

def ask_questions_node(state: AgentState) -> AgentState:
    """
    Generates clarifying questions based on missing information.
    """
    print("---ASK QUESTIONS NODE---")
    
    analysis = state['analysis']
    missing_info = analysis.get("missing_info", [])
    suggested_questions = analysis.get("suggested_questions", [])
    
    if suggested_questions:
        response_content = "I'd love to help you create a comprehensive product specification! To make sure I capture everything correctly, could you help me with a few details?\n\n"
        for i, question in enumerate(suggested_questions, 1):
            response_content += f"{i}. {question}\n"
        response_content += "\nFeel free to answer any or all of these - the more details you provide, the better I can help!"
    else:
        response_content = f"To create a complete specification, I need more information about: {', '.join(missing_info)}. Could you provide more details on these aspects?"
    
    # Add assistant message to conversation
    state['messages'].append({
        "role": "assistant", 
        "content": response_content
    })
    state['last_action'] = "ask_questions"
    
    return state

def knowledge_retrieval_node(state: AgentState) -> AgentState:
    """
    Retrieves expert knowledge from the knowledge base using RAG.
    Enhanced to use the domain-specific tools from tools.py.
    """
    print("---KNOWLEDGE RETRIEVAL NODE---")
    
    current_message = state['messages'][-1]['content']
    
    # Determine if this is a domain-specific or entity-specific query
    message_lower = current_message.lower()
    
    if any(term in message_lower for term in ['what is', 'tell me about', 'explain']):
        # Might be an entity search
        # Extract potential entity name (simplified logic)
        words = current_message.split()
        potential_entity = ' '.join([w for w in words if w.lower() not in ['what', 'is', 'tell', 'me', 'about', 'explain', 'the', 'a', 'an']])
        
        if len(potential_entity.split()) <= 3:  # Likely an entity
            retrieved_context = knowledge_base_entity_search_tool.func(potential_entity)
        else:
            retrieved_context = knowledge_base_retriever_tool.func(current_message)
    
    elif any(domain in message_lower for domain in ['material', 'fabric', 'manufacturing', 'process', 'compliance']):
        # Domain-specific search
        if 'material' in message_lower or 'fabric' in message_lower:
            retrieved_context = knowledge_base_domain_search_tool.func(current_message, "materials")
        elif 'manufacturing' in message_lower or 'process' in message_lower:
            retrieved_context = knowledge_base_domain_search_tool.func(current_message, "manufacturing")
        elif 'compliance' in message_lower:
            retrieved_context = knowledge_base_domain_search_tool.func(current_message, "compliance")
        else:
            retrieved_context = knowledge_base_retriever_tool.func(current_message)
    else:
        # General knowledge search
        retrieved_context = knowledge_base_retriever_tool.func(current_message)
    
    # Update state with retrieved context
    state['retrieved_context'] = retrieved_context
    state['last_action'] = "knowledge_retrieval"
    
    # Add response with the retrieved knowledge
    state['messages'].append({
        "role": "assistant",
        "content": f"Based on my knowledge base, here's what I found:\n\n{retrieved_context}\n\nWould you like me to help you apply this information to your product specification?"
    })
    
    return state

def dpg_update_node(state: AgentState) -> AgentState:
    """
    Updates the DPG with new information from the conversation.
    Uses the enhanced dpg_updater_tool from tools.py.
    """
    print("---DPG UPDATE NODE---")
    
    current_dpg = state.get('dpg_in_progress', {})
    new_info = state['messages'][-1]['content']
    
    # Add any retrieved context to the update
    if state.get('retrieved_context'):
        new_info += f"\n\n---Expert Context---\n{state['retrieved_context']}"
    
    if not current_dpg or not current_dpg.get('data'):
        # Create new DPG if none exists
        logger.info("Creating new DPG")
        updated_dpg = dpg_builder_tool.func(new_info)
        action_message = "I've created a new Digital Product Genome based on your information."
    else:
        # Update existing DPG using the enhanced tool from tools.py
        logger.info("Updating existing DPG")
        updated_dpg = dpg_updater_tool.func(current_dpg, new_info)
        action_message = "I've updated your Digital Product Genome with the new information."
    
    # Update state
    state['dpg_in_progress'] = updated_dpg
    state['messages'].append({
        "role": "assistant",
        "content": f"{action_message} You can view the updated specification in your product workspace. Is there anything else you'd like to add or modify?"
    })
    state['last_action'] = "dpg_update"
    
    return state

def rfq_generation_node(state: AgentState) -> AgentState:
    """
    Generates an RFQ based on the current DPG.
    """
    print("---RFQ GENERATION NODE---")
    
    dpg_data = state.get('dpg_in_progress', {})
    
    if not dpg_data or not dpg_data.get('data'):
        response_content = "I need a product specification (DPG) before I can generate an RFQ. Would you like me to create one first based on your product information?"
    else:
        # Generate RFQ using the enhanced tool from tools.py
        rfq_data = rfq_generator_tool.func(dpg_data)
        
        if rfq_data.get('status') == 'error':
            response_content = f"I encountered an error generating the RFQ: {rfq_data.get('error', 'Unknown error')}. Please try again or provide more product details."
        else:
            response_content = "I've generated a professional RFQ based on your product specification. The RFQ includes detailed technical requirements, quality standards, and submission guidelines that suppliers can use to provide accurate quotes."
            
            # Store RFQ in context
            if 'rfqs_created' not in state['conversation_context']:
                state['conversation_context']['rfqs_created'] = []
            state['conversation_context']['rfqs_created'].append(rfq_data)
    
    state['messages'].append({
        "role": "assistant",
        "content": response_content
    })
    state['last_action'] = "rfq_generation"
    
    return state

def supplier_discovery_node(state: AgentState) -> AgentState:
    """
    Discovers suppliers based on product requirements.
    """
    print("---SUPPLIER DISCOVERY NODE---")
    
    current_message = state['messages'][-1]['content']
    dpg_data = state.get('dpg_in_progress', {})
    
    # Extract product category from DPG or message
    product_category = "general product"
    if dpg_data and dpg_data.get('data', {}).get('category'):
        product_category = dpg_data['data']['category']
    elif dpg_data and dpg_data.get('data', {}).get('product_title'):
        product_category = dpg_data['data']['product_title']
    else:
        # Extract from current message
        product_category = current_message
    
    # Use supplier discovery tool from tools.py
    supplier_info = supplier_discovery_tool.func(product_category, "global")
    
    state['messages'].append({
        "role": "assistant",
        "content": f"I've found potential suppliers for your product:\n\n{supplier_info}"
    })
    state['last_action'] = "supplier_discovery"
    
    return state

def compliance_check_node(state: AgentState) -> AgentState:
    """
    Checks compliance requirements for the product.
    """
    print("---COMPLIANCE CHECK NODE---")
    
    dpg_data = state.get('dpg_in_progress', {})
    current_message = state['messages'][-1]['content']
    
    # Extract product category and target markets
    product_category = "general product"
    if dpg_data and dpg_data.get('data', {}).get('category'):
        product_category = dpg_data['data']['category']
    elif dpg_data and dpg_data.get('data', {}).get('product_title'):
        product_category = dpg_data['data']['product_title']
    
    # Default target markets, could be extracted from message or DPG
    target_markets = ["US", "EU"]
    
    # Use compliance checker tool from tools.py
    compliance_info = compliance_checker_tool.func(product_category, target_markets)
    
    state['messages'].append({
        "role": "assistant",
        "content": f"Here are the compliance requirements for your product:\n\n{compliance_info}"
    })
    state['last_action'] = "compliance_check"
    
    return state

def image_analysis_node(state: AgentState) -> AgentState:
    """
    Analyzes uploaded images for product development insights.
    """
    print("---IMAGE ANALYSIS NODE---")
    
    image_data = state.get('image_data')
    current_message = state['messages'][-1]['content']
    
    if not image_data:
        response_content = "I don't see any image data to analyze. Please upload an image and try again."
    else:
        # Use image analyzer tool from tools.py
        analysis_prompt = f"Analyze this product image for manufacturing and design details: {current_message}"
        analysis_result = image_analyzer_tool.func(image_data, analysis_prompt)
        response_content = f"Here's my analysis of the uploaded image:\n\n{analysis_result}"
    
    state['messages'].append({
        "role": "assistant",
        "content": response_content
    })
    state['last_action'] = "image_analysis"
    
    return state

def web_search_node(state: AgentState) -> AgentState:
    """
    Performs web search for current market information.
    """
    print("---WEB SEARCH NODE---")
    
    current_message = state['messages'][-1]['content']
    
    # Use web search tool from tools.py
    search_results = web_search_tool.func(current_message)
    
    state['search_results'] = search_results
    state['messages'].append({
        "role": "assistant",
        "content": f"I found current market information:\n\n{search_results}"
    })
    state['last_action'] = "web_search"
    
    return state

def file_processing_node(state: AgentState) -> AgentState:
    """
    Processes uploaded files and extracts information.
    """
    print("---FILE PROCESSING NODE---")
    
    file_outputs = state.get('file_outputs', [])
    
    if not file_outputs:
        response_content = "I don't see any files to process. Please upload files and try again."
    else:
        # Process file content and potentially update DPG
        extracted_content = ""
        successful_files = []
        
        for file_output in file_outputs:
            if file_output.get('status') == 'success':
                extracted_text = file_output.get('extracted_text', '')
                if extracted_text.strip():
                    extracted_content += f"\n=== {file_output.get('filename', 'Unknown File')} ===\n{extracted_text[:500]}...\n"
                    successful_files.append(file_output.get('filename', 'Unknown'))
        
        if extracted_content.strip():
            response_content = f"I've successfully processed {len(successful_files)} file(s): {', '.join(successful_files)}\n\nExtracted information:\n{extracted_content}\n\nWould you like me to use this information to update your product specification?"
        else:
            response_content = "I processed the files but couldn't extract meaningful text content. Please check the file format and try again."
    
    state['messages'].append({
        "role": "assistant",
        "content": response_content
    })
    state['last_action'] = "file_processing"
    
    return state

def general_response_node(state: AgentState) -> AgentState:
    """
    Handles general questions and conversation.
    Enhanced to be more contextually aware.
    """
    print("---GENERAL RESPONSE NODE---")
    
    general_llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0.3
    )
    
    current_message = state['messages'][-1]['content']
    context = state.get('conversation_context', {})
    
    # Build context-aware prompt
    context_info = ""
    if context.get('files_processed'):
        context_info += f"Files processed: {len(context['files_processed'])} files. "
    if state.get('dpg_in_progress') and state['dpg_in_progress'].get('data'):
        context_info += "Current DPG in progress. "
    if state.get('retrieved_context'):
        context_info += "Expert knowledge available. "
    
    # Check if user is asking about knowledge base
    message_lower = current_message.lower()
    if any(term in message_lower for term in ['knowledge base', 'what do you know', 'database', 'stats']):
        # Use knowledge base stats tool
        kb_stats = knowledge_base_stats_tool.func()
        response_content = f"Here's information about my knowledge base:\n\n{kb_stats}\n\nI can help you search for specific information about materials, manufacturing processes, compliance requirements, and more. What would you like to know?"
    else:
        prompt = f"""You are Unarchived AI, a helpful product development assistant with access to expert knowledge and advanced tools.

Context: {context_info}

User message: {current_message}

Provide a helpful, conversational response. If appropriate, suggest next steps like:
- Creating or updating a DPG (product specification)
- Searching the knowledge base for expert information
- Generating an RFQ for suppliers
- Finding suppliers or checking compliance
- Analyzing uploaded files or images

Be friendly, professional, and suggest specific actions the user can take."""
        
        response = general_llm.invoke(prompt)
        response_content = response.content
    
    state['messages'].append({
        "role": "assistant",
        "content": response_content
    })
    state['last_action'] = "general_response"
    
    return state

# Enhanced Router function
def route_after_controller(state: AgentState) -> str:
    """
    Routes to the appropriate node based on controller analysis.
    Enhanced to handle all available tools and capabilities.
    """
    action = state['analysis'].get("recommended_action", "general_response")
    current_message = state['messages'][-1]['content'].lower() if state['messages'] else ""
    
    # Enhanced routing logic
    routing_map = {
        "ask_questions": "ask_questions",
        "create_dpg": "dpg_update",
        "update_dpg": "dpg_update", 
        "create_rfq": "rfq_generation",
        "process_file": "file_processing",
        "knowledge_retrieval": "knowledge_retrieval",
        "supplier_discovery": "supplier_discovery",
        "compliance_check": "compliance_check",
        "image_analysis": "image_analysis",
        "web_search": "web_search",
        "general_response": "general_response"
    }
    
    # Additional routing logic based on content patterns
    if any(term in current_message for term in ["what is", "tell me about", "explain", "define"]):
        next_node = "knowledge_retrieval"
    elif any(term in current_message for term in ["supplier", "manufacturer", "find", "source"]):
        next_node = "supplier_discovery"
    elif any(term in current_message for term in ["compliance", "regulation", "standard", "requirement"]):
        next_node = "compliance_check"
    elif any(term in current_message for term in ["price", "cost", "market", "trend"]):
        next_node = "web_search"
    elif any(term in current_message for term in ["knowledge base", "stats", "database"]):
        next_node = "general_response"  # Will handle KB stats internally
    else:
        next_node = routing_map.get(action, "general_response")
    
    logger.info(f"Routing to: {next_node} (action: {action})")
    return next_node

# Build the Enhanced LangGraph workflow
workflow = StateGraph(AgentState)

# Add all nodes
workflow.add_node("controller", controller_node)
workflow.add_node("ask_questions", ask_questions_node)
workflow.add_node("knowledge_retrieval", knowledge_retrieval_node)
workflow.add_node("dpg_update", dpg_update_node)
workflow.add_node("rfq_generation", rfq_generation_node)
workflow.add_node("supplier_discovery", supplier_discovery_node)
workflow.add_node("compliance_check", compliance_check_node)
workflow.add_node("image_analysis", image_analysis_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("file_processing", file_processing_node)
workflow.add_node("general_response", general_response_node)

# Set entry point
workflow.set_entry_point("controller")

# Add conditional routing
workflow.add_conditional_edges(
    "controller",
    route_after_controller,
    {
        "ask_questions": "ask_questions",
        "knowledge_retrieval": "knowledge_retrieval",
        "dpg_update": "dpg_update",
        "rfq_generation": "rfq_generation", 
        "supplier_discovery": "supplier_discovery",
        "compliance_check": "compliance_check",
        "image_analysis": "image_analysis",
        "web_search": "web_search",
        "file_processing": "file_processing",
        "general_response": "general_response"
    }
)

# All nodes lead to END (single-turn interactions)
workflow.add_edge("ask_questions", END)
workflow.add_edge("knowledge_retrieval", END)
workflow.add_edge("dpg_update", END)
workflow.add_edge("rfq_generation", END)
workflow.add_edge("supplier_discovery", END)
workflow.add_edge("compliance_check", END)
workflow.add_edge("image_analysis", END)
workflow.add_edge("web_search", END)
workflow.add_edge("file_processing", END)
workflow.add_edge("general_response", END)

# Compile the graph
app = workflow.compile()

class ConversationalAgent:
    """
    Enhanced conversational agent with explicit state management and LangGraph integration.
    Fully synchronized with all tools from tools.py.
    """
    
    def __init__(self, user=None, dpg_id: int = None):
        self.user = user
        self.conversation_history = []
        self.context = {
            "dpgs_created": [],
            "rfqs_created": [],
            "files_processed": [],
            "product_info": {}
        }
        
        # Initialize DPG state
        self.current_dpg_id = dpg_id
        self.current_dpg_data = {}
        
        if dpg_id:
            # In a real implementation, you'd load from database
            self.current_dpg_data = DigitalProductGenome.objects.get(id=dpg_id).data
            logger.info(f"Initialized agent with DPG ID: {dpg_id}")
    
    def _prepare_initial_state(self, user_message: str, files: List[Dict] = None, image_data: str = None) -> AgentState:
        """
        Prepares the initial state for the LangGraph execution.
        Enhanced to handle images and all file types.
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Process files if provided
        file_outputs = []
        if files:
            file_outputs = self._process_files(files)
            # Enhance message with file content
            if file_outputs:
                file_content = self._extract_file_content_summary(file_outputs)
                enhanced_message = f"{user_message}\n\nUploaded files content:\n{file_content}"
                self.conversation_history[-1]["content"] = enhanced_message
        
        return AgentState(
            messages=self.conversation_history.copy(),
            dpg_in_progress=self.current_dpg_data.copy(),
            dpg_id=self.current_dpg_id,
            analysis={},
            retrieved_context="",
            last_action="start",
            file_outputs=file_outputs,
            conversation_context=self.context.copy(),
            image_data=image_data,
            search_results=None
        )
    
    def _process_files(self, files: List[Dict]) -> List[Dict]:
        """Process uploaded files using the enhanced file parser."""
        file_results = []
        
        for file_info in files:
            try:
                filename = file_info.get("filename", "unknown")
                content = file_info.get("content", "")
                content_type = file_info.get("content_type", "application/octet-stream")
                
                logger.info(f"Processing file: {filename}")
                
                # Use the enhanced file parser from tools.py
                result = file_parser_tool_base64.func(
                    content=content,
                    filename=filename,
                    content_type=content_type
                )
                
                file_results.append({
                    "filename": filename,
                    "status": "success" if result.get("success") else "error",
                    "extracted_text": result.get("extracted_text", ""),
                    "content_type": content_type,
                    "metadata": result.get("metadata", {})
                })
                
                self.context["files_processed"].append(filename)
                
            except Exception as e:
                logger.error(f"Failed to process file {file_info.get('filename', 'unknown')}: {str(e)}")
                file_results.append({
                    "filename": file_info.get("filename", "unknown"),
                    "status": "error",
                    "error": str(e)
                })
        
        return file_results
    
    def _extract_file_content_summary(self, file_outputs: List[Dict]) -> str:
        """Extract and summarize content from processed files."""
        content_summary = ""
        for file_result in file_outputs:
            if file_result.get("status") == "success" and file_result.get("extracted_text"):
                content_summary += f"\n=== {file_result['filename']} ===\n{file_result['extracted_text'][:500]}...\n"
        return content_summary
    
    
    
    @transaction.atomic
    def chat(self, message: str, files: List[Dict] = None, dpg_id: int = None, image_data: str = None) -> Dict[str, Any]:
        """
        Main chat interface using the enhanced LangGraph architecture.
        Now supports all tools and capabilities from tools.py.
        """
        try:
            # Update DPG ID if provided
            if dpg_id:
                self.current_dpg_id = dpg_id
                # In production, load from database:
                # self.current_dpg_data = DigitalProductGenome.objects.get(id=dpg_id).data
            
            # Prepare initial state (enhanced)
            initial_state = self._prepare_initial_state(message, files, image_data)
            
            # Execute the graph
            config = RunnableConfig(
                configurable={"thread_id": f"user_{getattr(self.user, 'id', 'anonymous')}"},
                metadata={
                    "user_id": str(getattr(self.user, 'id', 'anonymous')),
                    "dpg_id": str(self.current_dpg_id) if self.current_dpg_id else None,
                }
            )
            
            final_state = app.invoke(initial_state, config=config)
            
            # Extract assistant response
            assistant_message = ""
            if final_state['messages']:
                last_message = final_state['messages'][-1]
                if last_message.get('role') == 'assistant':
                    assistant_message = last_message.get('content', '')
            
            # Update internal state
            self.conversation_history = final_state['messages']
            self.current_dpg_data = final_state.get('dpg_in_progress', {})
            
            # Update context
            self.context.update(final_state.get('conversation_context', {}))
            
            # In production, save to database if DPG was updated
            updated_dpg_data = final_state.get('dpg_in_progress')
            if updated_dpg_data and self.user:
                # Placeholder for database save logic
                # if self.current_dpg_id:
                #     dpg_obj = DigitalProductGenome.objects.get(id=self.current_dpg_id)
                #     dpg_obj.data = updated_dpg_data
                #     dpg_obj.save()
                # else:
                #     new_dpg = DigitalProductGenome.objects.create(
                #         owner=self.user,
                #         data=updated_dpg_data
                #     )
                #     self.current_dpg_id = new_dpg.id
                pass
            
            return {
                "response": assistant_message,
                "dpg_id": self.current_dpg_id,
                "dpg_updated": bool(final_state.get('dpg_in_progress')),
                "last_action": final_state.get('last_action'),
                "analysis": final_state.get('analysis', {}),
                "file_results": final_state.get('file_outputs', []),
                "context": self.context,
                "suggestions": self._generate_suggestions(final_state),
                "retrieved_context": final_state.get('retrieved_context'),
                "search_results": final_state.get('search_results')
            }
            
        except Exception as e:
            logger.error(f"Agent processing error: {str(e)}")
            error_response = f"I encountered an error processing your request: {str(e)}. Please try again or contact support."
            
            self.conversation_history.append({"role": "assistant", "content": error_response})
            
            return {
                "response": error_response,
                "error": str(e),
                "context": self.context,
                "suggestions": ["Try rephrasing your request", "Upload different files", "Contact support"]
            }
    
    def _generate_suggestions(self, final_state: AgentState) -> List[str]:
        """Generate contextual suggestions based on current state and all available capabilities."""
        suggestions = []
        last_action = final_state.get('last_action')
        dpg_exists = bool(final_state.get('dpg_in_progress') and final_state.get('dpg_in_progress', {}).get('data'))
        
        if last_action == "ask_questions":
            suggestions.extend([
                "📝 Provide more product details",
                "📄 Upload product images or documents",
                "🔍 Search for material information"
            ])
            
        elif last_action == "dpg_update":
            suggestions.extend([
                "✅ Review the updated specification",
                "📄 Generate RFQ for suppliers",
                "🔧 Make additional modifications",
                "🏭 Find suppliers for this product"
            ])
            
        elif last_action == "knowledge_retrieval":
            suggestions.extend([
                "📋 Apply this info to my product spec",
                "🔍 Search for more specific details",
                "📊 Update my DPG with this knowledge"
            ])
            
        elif last_action == "supplier_discovery":
            suggestions.extend([
                "📄 Generate RFQ to send to suppliers",
                "✅ Check compliance requirements",
                "💰 Get current market pricing"
            ])
            
        elif dpg_exists and last_action != "rfq_generation":
            suggestions.extend([
                "📄 Generate RFQ for suppliers",
                "📊 Get DPG summary",
                "🏭 Find suppliers for this product",
                "✅ Check compliance requirements"
            ])
            
        elif last_action == "rfq_generation":
            suggestions.extend([
                "🏭 Find suppliers to send RFQ to",
                "✅ Review compliance requirements",
                "📊 Get market pricing information"
            ])
            
        elif last_action == "compliance_check":
            suggestions.extend([
                "📋 Update DPG with compliance info",
                "🔍 Find compliant suppliers",
                "📄 Generate updated RFQ"
            ])
            
        elif last_action == "web_search":
            suggestions.extend([
                "📋 Apply market data to my spec",
                "🏭 Find suppliers based on search",
                "💰 Update pricing estimates"
            ])
        
        # General suggestions if no DPG exists
        if not dpg_exists:
            suggestions.extend([
                "🚀 Create a new product specification",
                "📄 Upload product documentation",
                "🖼️ Upload product images for analysis"
            ])
        
        # Always available suggestions
        suggestions.extend([
            "❓ Ask about materials or processes",
            "🔍 Search for current market info",
            "📊 Check knowledge base stats"
        ])
        
        return suggestions[:6]  # Limit to 6 suggestions for UI
    
    def get_conversation_summary(self) -> str:
        """Get summary of current conversation state."""
        return f"""
**Agent State Summary:**
- Messages: {len(self.conversation_history)}
- Current DPG ID: {self.current_dpg_id}
- DPG Data: {'Present' if self.current_dpg_data else 'None'}
- Files Processed: {len(self.context.get('files_processed', []))}
- Available Tools: {len(tools)} tools integrated
- Last Action: {getattr(self, '_last_action', 'None')}

**Available Capabilities:**
- Create and update Digital Product Genomes (DPGs)
- Generate professional RFQs
- Search expert knowledge base (materials, processes, compliance)
- Find suppliers and check compliance requirements
- Analyze product images and process documents
- Perform current market research
"""

    def get_dpg_summary(self) -> str:
        """Get a summary of the current DPG using the dpg_summary_tool."""
        if not self.current_dpg_data or not self.current_dpg_data.get('data'):
            return "No DPG currently available. Create one by describing your product!"
        
        try:
            summary = dpg_summary_tool.func(self.current_dpg_data)
            return summary
        except Exception as e:
            logger.error(f"Error generating DPG summary: {str(e)}")
            return f"Error generating DPG summary: {str(e)}"

# Backwards compatibility function (enhanced)
def chat_session(messages: list, files: List[Dict] = None, image_data: str = None) -> dict:
    """Backwards compatible chat session function with enhanced capabilities."""
    agent = ConversationalAgent()
    
    # Build conversation history
    for msg in messages[:-1]:
        agent.conversation_history.append(msg)
    
    # Process last message with all enhancements
    if messages:
        last_message = messages[-1]
        result = agent.chat(
            message=last_message.get("content", ""),
            files=files,
            image_data=image_data
        )
        return {
            "messages": agent.conversation_history,
            "response": result.get("response", ""),
            "context": result.get("context", {}),
            "dpg_id": result.get("dpg_id"),
            "suggestions": result.get("suggestions", []),
            "analysis": result.get("analysis", {}),
            "last_action": result.get("last_action"),
            "file_results": result.get("file_results", []),
            "retrieved_context": result.get("retrieved_context"),
            "search_results": result.get("search_results")
        }
    
    return {
        "messages": [], 
        "response": "No messages provided", 
        "context": {},
        "suggestions": ["🚀 Start by describing your product idea"]
    }

# Utility functions for external use
def create_agent(user=None, dpg_id=None) -> ConversationalAgent:
    """Factory function to create a new agent instance."""
    return ConversationalAgent(user=user, dpg_id=dpg_id)

def get_knowledge_base_stats() -> str:
    """Get knowledge base statistics using the stats tool."""
    try:
        return knowledge_base_stats_tool.func()
    except Exception as e:
        logger.error(f"Error getting KB stats: {str(e)}")
        return f"Error retrieving knowledge base statistics: {str(e)}"

def search_knowledge_base(query: str, domain: str = None) -> str:
    """Search the knowledge base with optional domain filtering."""
    try:
        if domain:
            return knowledge_base_domain_search_tool.func(query, domain)
        else:
            return knowledge_base_retriever_tool.func(query)
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        return f"Error searching knowledge base: {str(e)}"

def find_entity_info(entity_name: str) -> str:
    """Find comprehensive information about a specific entity."""
    try:
        return knowledge_base_entity_search_tool.func(entity_name)
    except Exception as e:
        logger.error(f"Error finding entity info: {str(e)}")
        return f"Error finding information for '{entity_name}': {str(e)}"