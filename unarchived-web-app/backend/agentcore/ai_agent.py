import openai
import json
from django.conf import settings
from typing import List, Dict, Any, Optional
#from .models import Supplier, RFQ, Quote
from suppliers.models import Supplier
from rfq.models import RFQ
from quotes.models import Quote

class SourcingAgent:
    """AI agent for sourcing assistance"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
        # System prompt for the sourcing agent
        self.system_prompt = """You are an expert AI sourcing assistant for Unarchived, a global sourcing platform. Your role is to help users find suppliers, get quotes, and manage their sourcing needs.

Key capabilities:
- Help users create detailed RFQs (Request for Quotes)
- Suggest relevant suppliers based on product requirements
- Provide sourcing advice and best practices
- Help analyze quotes and supplier capabilities
- Guide users through the sourcing process

Always be helpful, professional, and provide actionable advice. When suggesting suppliers or creating RFQs, be specific and detailed. Use markdown formatting for better readability.

Current platform features:
- Global supplier network with 50,000+ verified suppliers
- Automated quote collection and comparison
- Escrow payment protection
- Quality assurance and inspection services
- Logistics and shipping coordination

Remember to ask clarifying questions when needed to provide the best sourcing recommendations."""

    def get_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> str:
        """Get AI response for user message"""
        try:
            # Prepare conversation history
            messages: List[Dict[str, str]] = [{"role": "system", "content": self.system_prompt}]
            
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    messages.append({
                        "role": "user" if msg["author"] == "user" else "assistant",
                        "content": msg["content"]
                    })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content or "I apologize, but I couldn't generate a response."
            
        except openai.AuthenticationError:
            return "I'm having trouble connecting to my AI service. Please check your API configuration."
        except openai.RateLimitError:
            return "I'm receiving too many requests right now. Please try again in a moment."
        except openai.APIError as e:
            return f"I'm experiencing technical difficulties: {str(e)}"
        except Exception as e:
            return "I apologize, but I'm having trouble processing your request. Please try again."

    def create_rfq_from_conversation(self, user_message: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Extract RFQ details from conversation and create structured RFQ"""
        try:
            # Prepare context for RFQ extraction
            context = f"""
            Based on the following conversation, extract RFQ details and create a structured RFQ:
            
            Conversation History:
            {json.dumps(conversation_history, indent=2)}
            
            Current Message: {user_message}
            
            Extract the following information in JSON format:
            - product_name: The product being sourced
            - quantity: Estimated quantity needed
            - specifications: Key specifications and requirements
            - target_price: Target price per unit (if mentioned)
            - deadline: Required delivery date (if mentioned)
            - regions: Preferred sourcing regions (if mentioned)
            - additional_notes: Any other important details
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at extracting RFQ details from conversations. Return only valid JSON."},
                    {"role": "user", "content": context}
                ],  # type: ignore
                max_tokens=500,
                temperature=0.3
            )
            
            # Parse the response
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")
                
            # Extract JSON from the response (in case it's wrapped in markdown)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            rfq_data = json.loads(content.strip())
            return rfq_data
            
        except openai.AuthenticationError:
            return {
                "error": "Authentication failed. Please check your API configuration.",
                "product_name": "Unknown",
                "quantity": 0,
                "specifications": "",
                "target_price": "",
                "deadline": "",
                "regions": [],
                "additional_notes": ""
            }
        except openai.RateLimitError:
            return {
                "error": "Rate limit exceeded. Please try again later.",
                "product_name": "Unknown",
                "quantity": 0,
                "specifications": "",
                "target_price": "",
                "deadline": "",
                "regions": [],
                "additional_notes": ""
            }
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse AI response. Please try again.",
                "product_name": "Unknown",
                "quantity": 0,
                "specifications": "",
                "target_price": "",
                "deadline": "",
                "regions": [],
                "additional_notes": ""
            }
        except Exception as e:
            return {
                "error": f"Failed to extract RFQ details: {str(e)}",
                "product_name": "Unknown",
                "quantity": 0,
                "specifications": "",
                "target_price": "",
                "deadline": "",
                "regions": [],
                "additional_notes": ""
            }

    def suggest_suppliers(self, product_name: str, specifications: str) -> List[Dict[str, Any]]:
        """Suggest relevant suppliers based on product requirements"""
        try:
            # Get actual suppliers from database
            suppliers = Supplier.objects.filter(  # type: ignore
                category__icontains=product_name.lower()
            )[:5]  # Get top 5 matches
            
            if not suppliers.exists():
                # If no exact matches, get some general suppliers
                suppliers = Supplier.objects.all()[:5]  # type: ignore
            
            supplier_suggestions = []
            for supplier in suppliers:
                supplier_suggestions.append({
                    "id": supplier.id,
                    "name": supplier.name,
                    "region": supplier.region,
                    "category": supplier.category,
                    "reliability": supplier.reliability,
                    "contact_email": supplier.contact_email,
                    "reason": f"Specializes in {supplier.category} with {supplier.reliability}% reliability"
                })
            
            return supplier_suggestions
            
        except Exception as e:
            return [{"error": f"Failed to suggest suppliers: {str(e)}"}]

    def analyze_quotes(self, quotes: List[Quote]) -> Dict[str, Any]:
        """Analyze and compare quotes"""
        try:
            if not quotes:
                return {"error": "No quotes to analyze"}
            
            # Prepare quote data for analysis
            quote_data = []
            for quote in quotes:
                quote_data.append({
                    "supplier": quote.supplier.name,
                    "price": str(quote.price),  # Convert Decimal to string
                    "lead_time": quote.lead_time,
                    "reliability": quote.supplier.reliability,  # type: ignore
                    "moq": quote.moq
                })
            
            # Create analysis prompt
            analysis_prompt = f"""
            Analyze the following quotes and provide recommendations:
            
            {json.dumps(quote_data, indent=2)}
            
            Provide analysis in JSON format with:
            - best_value: Supplier with best price-quality ratio
            - fastest_delivery: Supplier with shortest lead time
            - highest_quality: Supplier with highest reliability
            - recommendations: List of recommendations
            - risk_assessment: Any potential risks
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert sourcing analyst. Provide detailed quote analysis in JSON format."},
                    {"role": "user", "content": analysis_prompt}
                ],  # type: ignore
                max_tokens=800,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")
                
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            analysis_result = json.loads(content.strip())
            return analysis_result
            
        except openai.AuthenticationError:
            return {"error": "Authentication failed. Please check your API configuration."}
        except openai.RateLimitError:
            return {"error": "Rate limit exceeded. Please try again later."}
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI analysis. Please try again."}
        except Exception as e:
            return {"error": f"Failed to analyze quotes: {str(e)}"}

# Create a singleton instance
sourcing_agent = SourcingAgent() 