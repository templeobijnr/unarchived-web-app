from typing import TypedDict, List, Dict, Any
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from decouple import config
from .tools import dpg_builder_tool, rfq_generator_tool, file_parser_tool_base64, dpg_summary_tool
from dpgs.models import DigitalProductGenome
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import json
import re

llm = ChatOpenAI(
    model_name=config("OPENAI_MODEL", default="gpt-4"),
    openai_api_key=config("OPENAI_API_KEY"),
    temperature=0.1  # Slightly higher for more natural conversation
)

# Enhanced system prompt for intelligent conversation handling
SYSTEM_PROMPT = """You are Unarchived Ai, an intelligent product development and sourcing assistant. Your role is to help brands and product managers with:

1. **File Processing**: Parse and extract information from uploaded files (images, PDFs, documents)
2. **Product Specification**: Create Digital Product Genomes (DPGs) from product information
3. **Sourcing Support**: Generate professional RFQs (Request for Quotes) for suppliers
4. **Conversational Guidance**: Answer questions and guide users through the product development process

**CONVERSATION INTELLIGENCE RULES:**

- **Listen and Learn**: Build context from the conversation before acting
- **Ask Clarifying Questions**: When product information is incomplete, ask specific questions
- **Suggest Next Steps**: Proactively recommend when to create DPGs or RFQs
- **File Processing**: Always process uploaded files first to extract information
- **Context Awareness**: Remember previous messages and build upon them

**WHEN TO CREATE A DPG:**
- User has provided sufficient product details (materials, design, features, etc.)
- User explicitly asks for a product specification or DPG
- After processing files that contain product information
- When user wants to formalize scattered product information

**WHEN TO CREATE AN RFQ:**
- A DPG already exists or has been created
- User explicitly asks for an RFQ or quote request
- User mentions needing to contact suppliers/manufacturers
- User asks about pricing or sourcing

**CONVERSATION STYLE:**
- Be helpful and professional but conversational
- Ask follow-up questions to gather missing information
- Explain what you're doing and why
- Suggest logical next steps in the product development process"""

@tool
def conversation_analyzer_tool(conversation_history: str, current_message: str) -> dict:
    """
    Analyzes the conversation to determine the best next action and what information might be missing.
    """
    analysis_llm = ChatOpenAI(
        model_name=config("OPENAI_MODEL", default="gpt-4"),
        openai_api_key=config("OPENAI_API_KEY"),
        temperature=0
    )
    
    prompt = f"""Analyze this conversation and determine:

1. What product information has been gathered so far?
2. What key information is still missing for creating a complete DPG?
3. Should we create a DPG now, ask for more info, or suggest an RFQ?
4. What specific questions should be asked next?

CONVERSATION HISTORY:
{conversation_history}

CURRENT MESSAGE:
{current_message}

Respond with JSON:
{{
    "product_info_gathered": {{"title": "string", "materials": [], "colors": [], "etc": "..."}},
    "missing_info": ["list of missing key information"],
    "recommended_action": "ask_questions|create_dpg|create_rfq|process_file|general_response",
    "confidence_level": "high|medium|low",
    "suggested_questions": ["specific questions to ask"],
    "reasoning": "explanation of recommendation"
}}"""
    
    try:
        response = analysis_llm.invoke(prompt)
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {"error": "Could not parse analysis response"}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

# Add the new tool to the tools list
tools = [file_parser_tool_base64, dpg_builder_tool, rfq_generator_tool, dpg_summary_tool, conversation_analyzer_tool]

# Enhanced agent state to track conversation context
class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    file_outputs: List[Dict[str, Any]]
    dpgs_created: List[Dict[str, Any]]
    rfqs_created: List[Dict[str, Any]]
    conversation_context: Dict[str, Any]

def intelligent_agent_node(state: AgentState) -> AgentState:
    """
    Enhanced agent node that makes intelligent decisions based on conversation context.
    """
    messages = state.get("messages", [])
    
    # Convert messages to LangChain format
    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
    
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
    
    # Use the react agent to process
    react_agent = create_react_agent(llm, tools)
    config = RunnableConfig()
    
    result = react_agent.invoke({"messages": lc_messages}, config=config)
    
    # Update state with any new information
    updated_state = state.copy()
    if "messages" in result:
        updated_state["messages"] = result["messages"]
    
    return updated_state

# Create the enhanced graph
graph = StateGraph(AgentState)
graph.add_node("intelligent_agent", intelligent_agent_node)
graph.set_entry_point("intelligent_agent")
graph.set_finish_point("intelligent_agent")

app = graph.compile()

class ConversationalAgent:
    """
    Enhanced conversational agent that maintains context and makes intelligent decisions.
    """
    
    def __init__(self):
        self.conversation_history = []
        self.context = {
            "dpgs_created": [],
            "rfqs_created": [],
            "files_processed": [],
            "product_info": {}
        }
    
    def chat(self, message: str, files: List[Dict] = None) -> Dict[str, Any]:
        """
        Main chat interface that handles messages and files intelligently.
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Process any uploaded files first
        file_results = []
        if files:
            for file_info in files:
                try:
                    result = file_parser_tool_base64.func(
                        content=file_info.get("content", ""),
                        filename=file_info.get("filename", ""),
                        content_type=file_info.get("content_type", "")
                    )
                    file_results.append(result)
                    self.context["files_processed"].append(file_info.get("filename", "unknown"))
                    
                    # Add file content to conversation context
                    if result.get("extracted_text"):
                        message += f"\n\n[File Content from {file_info.get('filename', 'uploaded file')}]:\n{result['extracted_text']}"
                        
                except Exception as e:
                    file_results.append({"error": f"Failed to process file: {str(e)}"})
        
        # Prepare state for the agent
        initial_state = {
            "messages": self.conversation_history,
            "file_outputs": file_results,
            "dpgs_created": self.context["dpgs_created"],
            "rfqs_created": self.context["rfqs_created"],
            "conversation_context": self.context
        }
        
        # Run the intelligent agent
        try:
            config = RunnableConfig()
            result = app.invoke(initial_state, config=config)
            
            # Extract the assistant's response
            assistant_message = ""
            if "messages" in result and result["messages"]:
                last_message = result["messages"][-1]
                if hasattr(last_message, 'content'):
                    assistant_message = last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    assistant_message = last_message["content"]
            
            # Add assistant response to history
            if assistant_message:
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Update context with any new DPGs or RFQs created
            self._update_context_from_result(result)
            
            return {
                "response": assistant_message,
                "file_results": file_results,
                "context": self.context,
                "suggestions": self._generate_suggestions()
            }
            
        except Exception as e:
            error_response = f"I encountered an error: {str(e)}. Could you please try again or rephrase your request?"
            self.conversation_history.append({"role": "assistant", "content": error_response})
            return {
                "response": error_response,
                "error": str(e),
                "context": self.context
            }
    
    def _update_context_from_result(self, result):
        """Update the conversation context based on agent results."""
        # This would be enhanced to detect when DPGs or RFQs are created
        # and update the context accordingly
        pass
    
    def _generate_suggestions(self) -> List[str]:
        """Generate helpful suggestions based on current context."""
        suggestions = []
        
        if not self.context["files_processed"] and not self.context["dpgs_created"]:
            suggestions.append("💡 Upload product images, documents, or specifications to get started")
        
        if self.context["files_processed"] and not self.context["dpgs_created"]:
            suggestions.append("📋 Ready to create a Digital Product Genome (DPG) from your uploaded files?")
        
        if self.context["dpgs_created"] and not self.context["rfqs_created"]:
            suggestions.append("📄 Generate an RFQ (Request for Quote) to send to suppliers")
        
        if len(self.context["dpgs_created"]) > 1:
            suggestions.append("🔄 Compare multiple DPGs or merge related products")
        
        return suggestions
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation and context."""
        summary = f"""
**Conversation Summary:**
- Messages exchanged: {len(self.conversation_history)}
- Files processed: {len(self.context['files_processed'])}
- DPGs created: {len(self.context['dpgs_created'])}
- RFQs generated: {len(self.context['rfqs_created'])}

**Files processed:** {', '.join(self.context['files_processed']) if self.context['files_processed'] else 'None'}
"""
        return summary

# Convenience function for backwards compatibility
def chat_session(messages: list) -> dict:
    """
    Backwards compatible chat session function.
    """
    agent = ConversationalAgent()
    
    # Process all messages except the last one to build context
    for msg in messages[:-1]:
        agent.conversation_history.append(msg)
    
    # Process the last message
    if messages:
        last_message = messages[-1]
        result = agent.chat(last_message.get("content", ""))
        return {
            "messages": agent.conversation_history,
            "response": result.get("response", ""),
            "context": result.get("context", {})
        }
    
    return {"messages": [], "response": "No messages provided", "context": {}}

# Example usage
if __name__ == "__main__":
    # Example of how to use the enhanced agent
    agent = ConversationalAgent()
    
    # Simulate a conversation
    response1 = agent.chat("Hi, I want to create a new handbag product. Can you help me?")
    print("Agent:", response1["response"])
    
    response2 = agent.chat("It's a leather crossbody bag with gold hardware and adjustable strap.")
    print("Agent:", response2["response"])
    
    # The agent would intelligently ask follow-up questions or suggest creating a DPG