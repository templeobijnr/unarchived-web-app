import openai
import json
import asyncio
from typing import List, Dict, Any, Optional
from django.conf import settings
from django.db import transaction
from .models import Supplier, RFQ, Quote, Message, KPI
from datetime import datetime, timedelta

class AdvancedSourcingAgent:
    """World-class AI sourcing agent for end-to-end procurement"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
        # System prompt for the advanced sourcing agent
        self.system_prompt = """You are an expert AI sourcing agent for Unarchived, a world-class global sourcing platform. You handle the complete end-to-end sourcing process from initial conversation to final delivery.

CORE CAPABILITIES:
1. PRODUCT UNDERSTANDING: Extract detailed specifications from natural language, images, or rough descriptions
2. SUPPLIER MATCHING: Find the best suppliers based on capability, quality, location, and reliability
3. RFQ GENERATION: Create comprehensive RFQs with technical specifications
4. QUOTE ANALYSIS: Compare quotes and provide data-driven recommendations
5. PROCESS MANAGEMENT: Handle orders, quality control, logistics, and payments
6. RISK ASSESSMENT: Evaluate and mitigate sourcing risks

CONVERSATION FLOW:
- Start by understanding the user's needs through natural conversation
- Ask clarifying questions to gather complete requirements
- Provide options and recommendations with explanations
- Handle objections and concerns professionally
- Guide users through each step of the process
- Keep users informed of progress and next steps

PLATFORM FEATURES:
- 50,000+ verified suppliers across 40+ countries
- Automated quality assurance and inspection services
- Escrow payment protection and milestone-based payments
- Real-time logistics tracking and customs handling
- Comprehensive risk management and insurance
- 24/7 support and dispute resolution

Always be helpful, professional, and proactive. Think several steps ahead and anticipate user needs. Provide specific, actionable advice with clear next steps."""

    async def process_conversation(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process user message and determine next actions"""
        try:
            # Analyze conversation intent and context
            intent_analysis = await self._analyze_intent(user_message, conversation_history)
            
            # Determine appropriate response and actions
            if intent_analysis['intent'] == 'product_inquiry':
                return await self._handle_product_inquiry(user_message, conversation_history, user_context)
            elif intent_analysis['intent'] == 'rfq_creation':
                return await self._handle_rfq_creation(user_message, conversation_history, user_context)
            elif intent_analysis['intent'] == 'quote_analysis':
                return await self._handle_quote_analysis(user_message, conversation_history, user_context)
            elif intent_analysis['intent'] == 'order_management':
                return await self._handle_order_management(user_message, conversation_history, user_context)
            elif intent_analysis['intent'] == 'general_question':
                return await self._handle_general_question(user_message, conversation_history, user_context)
            else:
                return await self._handle_unknown_intent(user_message, conversation_history, user_context)
                
        except openai.AuthenticationError:
            return {
                'response': "I'm having trouble connecting to my AI service. Please check your API configuration.",
                'actions': [],
                'next_steps': ['Contact support if the issue persists']
            }
        except openai.RateLimitError:
            return {
                'response': "I'm receiving too many requests right now. Please try again in a moment.",
                'actions': [],
                'next_steps': ['Wait a few minutes and try again']
            }
        except openai.APIError as e:
            return {
                'response': f"I'm experiencing technical difficulties: {str(e)}",
                'actions': [],
                'next_steps': ['Try again later or contact support']
            }
        except Exception as e:
            return {
                'response': f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}",
                'actions': [],
                'next_steps': ['Contact support if the issue persists']
            }

    async def _analyze_intent(self, user_message: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Analyze user intent and extract key information"""
        try:
            analysis_prompt = f"""
            Analyze the following user message and conversation history to determine intent and extract key information:
            
            User Message: {user_message}
            Conversation History: {json.dumps(conversation_history[-5:], indent=2)}
            
            Return analysis in JSON format:
            {{
                "intent": "product_inquiry|rfq_creation|quote_analysis|order_management|general_question",
                "confidence": 0.0-1.0,
                "extracted_info": {{
                    "product_type": "string",
                    "quantity": "number or range",
                    "specifications": ["list of specs"],
                    "timeline": "string",
                    "budget": "string",
                    "location": "string"
                }},
                "missing_info": ["list of missing details"],
                "suggested_questions": ["questions to ask user"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing sourcing conversations and extracting intent."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            return json.loads(content.strip())
            
        except openai.AuthenticationError:
            return {
                "intent": "general_question",
                "confidence": 0.5,
                "extracted_info": {},
                "missing_info": [],
                "suggested_questions": ["Could you tell me more about what you're looking for?"]
            }
        except openai.RateLimitError:
            return {
                "intent": "general_question",
                "confidence": 0.5,
                "extracted_info": {},
                "missing_info": [],
                "suggested_questions": ["Could you tell me more about what you're looking for?"]
            }
        except json.JSONDecodeError:
            return {
                "intent": "general_question",
                "confidence": 0.5,
                "extracted_info": {},
                "missing_info": [],
                "suggested_questions": ["Could you tell me more about what you're looking for?"]
            }
        except Exception as e:
            return {
                "intent": "general_question",
                "confidence": 0.5,
                "extracted_info": {},
                "missing_info": [],
                "suggested_questions": ["Could you tell me more about what you're looking for?"]
            }

    async def _handle_product_inquiry(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict]) -> Dict[str, Any]:
        """Handle initial product inquiries and gather requirements"""
        try:
            # Extract product information
            product_info = await self._extract_product_info(user_message, conversation_history)
            
            # Generate response with next steps
            response_prompt = f"""
            The user is inquiring about sourcing a product. Here's what we know:
            
            Product Info: {json.dumps(product_info, indent=2)}
            User Message: {user_message}
            
            Provide a helpful response that:
            1. Acknowledges their inquiry
            2. Shows understanding of their needs
            3. Asks relevant clarifying questions
            4. Explains how we can help
            5. Sets expectations for the process
            
            Be conversational, professional, and encouraging.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": response_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content or "I understand you're looking for sourcing assistance. Let me help you with that."
            
            return {
                'response': ai_response,
                'actions': [
                    {
                        'type': 'extract_requirements',
                        'data': product_info,
                        'priority': 'high'
                    }
                ],
                'next_steps': [
                    'Gather complete product specifications',
                    'Determine quantity and timeline',
                    'Identify quality requirements',
                    'Establish budget constraints'
                ]
            }
            
        except openai.AuthenticationError:
            return {
                'response': "I'd be happy to help you source that product. Could you tell me more about your requirements?",
                'actions': [],
                'next_steps': ['Gather more information about the product']
            }
        except openai.RateLimitError:
            return {
                'response': "I'd be happy to help you source that product. Could you tell me more about your requirements?",
                'actions': [],
                'next_steps': ['Gather more information about the product']
            }
        except Exception as e:
            return {
                'response': "I'd be happy to help you source that product. Could you tell me more about your requirements?",
                'actions': [],
                'next_steps': ['Gather more information about the product']
            }

    async def _handle_rfq_creation(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict]) -> Dict[str, Any]:
        """Handle RFQ creation from conversation"""
        try:
            # Extract complete RFQ details
            rfq_data = await self._extract_rfq_details(user_message, conversation_history)
            
            # Create RFQ in database
            with transaction.atomic():
                rfq = RFQ.objects.create(
                    title=rfq_data.get('product_name', 'New RFQ'),
                    description=rfq_data.get('specifications', ''),
                    category=rfq_data.get('product_type', 'General'),
                    quantity=rfq_data.get('quantity', 1),
                    target_price=rfq_data.get('target_price', 0),
                    deadline=datetime.now() + timedelta(days=30),
                    created_by=user_context.get('user') if user_context else None
                )
            
            return {
                'response': f"Perfect! I've created an RFQ for {rfq_data.get('product_name', 'your product')}. I'll start matching you with qualified suppliers right away.",
                'actions': [
                    {
                        'type': 'create_rfq',
                        'data': {'rfq_id': rfq.id},
                        'priority': 'high'
                    }
                ],
                'next_steps': [
                    'Supplier matching in progress',
                    'Quotes expected within 24-48 hours',
                    'Review and compare quotes',
                    'Select best supplier'
                ]
            }
            
        except openai.AuthenticationError:
            return {
                'response': "I'm having trouble processing your request right now. Please try again in a moment.",
                'actions': [],
                'next_steps': ['Retry RFQ creation']
            }
        except openai.RateLimitError:
            return {
                'response': "I'm receiving too many requests. Please try again in a moment.",
                'actions': [],
                'next_steps': ['Retry RFQ creation']
            }
        except Exception as e:
            return {
                'response': "I encountered an issue creating your RFQ. Please try again or contact support.",
                'actions': [],
                'next_steps': ['Retry RFQ creation or contact support']
            }

    async def _handle_quote_analysis(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict]) -> Dict[str, Any]:
        """Handle quote analysis requests"""
        try:
            # Get quotes for analysis
            quotes = Quote.objects.filter(status='pending')[:10]  # Get recent quotes
            
            if not quotes.exists():
                return {
                    'response': "I don't see any quotes to analyze yet. Let me help you create an RFQ to get some quotes.",
                    'actions': [
                        {
                            'type': 'create_rfq',
                            'data': {},
                            'priority': 'medium'
                        }
                    ],
                    'next_steps': ['Create an RFQ', 'Wait for supplier responses', 'Analyze quotes']
                }
            
            # Analyze quotes using AI
            analysis_result = await self._analyze_quotes_advanced(quotes)
            
            return {
                'response': f"I've analyzed {len(quotes)} quotes for you. Here's my recommendation: {analysis_result.get('recommendations', 'Review all options carefully.')}",
                'actions': [
                    {
                        'type': 'analyze_quotes',
                        'data': analysis_result,
                        'priority': 'high'
                    }
                ],
                'next_steps': [
                    'Review detailed analysis',
                    'Compare supplier options',
                    'Select preferred supplier',
                    'Proceed with order'
                ]
            }
            
        except openai.AuthenticationError:
            return {
                'response': "I'm having trouble analyzing quotes right now. Please try again in a moment.",
                'actions': [],
                'next_steps': ['Retry quote analysis']
            }
        except openai.RateLimitError:
            return {
                'response': "I'm receiving too many requests. Please try again in a moment.",
                'actions': [],
                'next_steps': ['Retry quote analysis']
            }
        except Exception as e:
            return {
                'response': "I encountered an issue analyzing quotes. Please try again or contact support.",
                'actions': [],
                'next_steps': ['Retry quote analysis or contact support']
            }

    async def _handle_order_management(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict]) -> Dict[str, Any]:
        """Handle order management requests"""
        try:
            # Extract order information
            order_info = await self._extract_order_info(user_message, conversation_history)
            
            return {
                'response': "I understand you want to manage your orders. Let me help you track and manage your sourcing projects.",
                'actions': [
                    {
                        'type': 'manage_orders',
                        'data': order_info,
                        'priority': 'medium'
                    }
                ],
                'next_steps': [
                    'View active orders',
                    'Track order progress',
                    'Handle any issues',
                    'Manage payments'
                ]
            }
            
        except openai.AuthenticationError:
            return {
                'response': "I'm having trouble accessing order information right now. Please try again in a moment.",
                'actions': [],
                'next_steps': ['Retry order management']
            }
        except openai.RateLimitError:
            return {
                'response': "I'm receiving too many requests. Please try again in a moment.",
                'actions': [],
                'next_steps': ['Retry order management']
            }
        except Exception as e:
            return {
                'response': "I encountered an issue with order management. Please try again or contact support.",
                'actions': [],
                'next_steps': ['Retry order management or contact support']
            }

    async def _handle_general_question(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict]) -> Dict[str, Any]:
        """Handle general questions about sourcing"""
        try:
            response_prompt = f"""
            The user has a general question about sourcing. Please provide a helpful response:
            
            User Question: {user_message}
            Conversation Context: {json.dumps(conversation_history[-3:], indent=2)}
            
            Provide a helpful, informative response that:
            1. Answers their question directly
            2. Provides additional useful information
            3. Offers to help with specific sourcing needs
            4. Encourages further engagement
            
            Be professional, knowledgeable, and encouraging.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": response_prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content or "I'd be happy to help you with your sourcing questions. What would you like to know?"
            
            return {
                'response': ai_response,
                'actions': [],
                'next_steps': ['Continue conversation', 'Ask follow-up questions']
            }
            
        except openai.AuthenticationError:
            return {
                'response': "I'd be happy to help you with your sourcing questions. What would you like to know?",
                'actions': [],
                'next_steps': ['Ask your question again']
            }
        except openai.RateLimitError:
            return {
                'response': "I'd be happy to help you with your sourcing questions. What would you like to know?",
                'actions': [],
                'next_steps': ['Ask your question again']
            }
        except Exception as e:
            return {
                'response': "I'd be happy to help you with your sourcing questions. What would you like to know?",
                'actions': [],
                'next_steps': ['Ask your question again']
            }

    async def _handle_unknown_intent(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict]) -> Dict[str, Any]:
        """Handle unknown or unclear user intent"""
        return {
            'response': "I'm not quite sure what you're looking for. Could you tell me more about your sourcing needs? I can help you find suppliers, create RFQs, analyze quotes, or answer any sourcing questions.",
            'actions': [],
            'next_steps': ['Clarify your requirements', 'Ask specific questions']
        }

    async def _extract_product_info(self, user_message: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Extract product information from conversation"""
        try:
            extraction_prompt = f"""
            Extract product information from this conversation:
            
            User Message: {user_message}
            Conversation History: {json.dumps(conversation_history[-3:], indent=2)}
            
            Return in JSON format:
            {{
                "product_type": "string",
                "product_name": "string",
                "specifications": ["list"],
                "quantity": "number or range",
                "materials": ["list"],
                "quality_requirements": "string",
                "timeline": "string",
                "budget": "string",
                "location": "string"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Extract product information accurately."},
                    {"role": "user", "content": extraction_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                return {}
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            return json.loads(content.strip())
            
        except Exception as e:
            return {}

    async def _extract_rfq_details(self, user_message: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Extract complete RFQ details from conversation"""
        try:
            extraction_prompt = f"""
            Extract complete RFQ details from this conversation:
            
            User Message: {user_message}
            Conversation History: {json.dumps(conversation_history[-5:], indent=2)}
            
            Return in JSON format:
            {{
                "product_name": "string",
                "product_type": "string",
                "quantity": "number",
                "specifications": "string",
                "target_price": "number",
                "deadline": "string",
                "quality_requirements": "string",
                "materials": ["list"],
                "certifications": ["list"],
                "packaging": "string",
                "shipping": "string"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Extract RFQ details accurately."},
                    {"role": "user", "content": extraction_prompt}
                ],
                max_tokens=600,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                return {}
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            return json.loads(content.strip())
            
        except Exception as e:
            return {}

    async def _analyze_quotes_advanced(self, quotes: List[Quote]) -> Dict[str, Any]:
        """Advanced quote analysis with multiple dimensions"""
        try:
            quote_data = []
            for quote in quotes:
                quote_data.append({
                    "supplier": quote.supplier.name,
                    "price": str(quote.price),
                    "lead_time": quote.lead_time,
                    "reliability": quote.supplier.reliability,
                    "moq": quote.moq,
                    "region": quote.supplier.region,
                    "certifications": quote.supplier.certifications
                })
            
            analysis_prompt = f"""
            Analyze these quotes comprehensively:
            
            {json.dumps(quote_data, indent=2)}
            
            Provide analysis in JSON format:
            {{
                "best_value": {{
                    "supplier": "string",
                    "reason": "string",
                    "score": "number"
                }},
                "fastest_delivery": {{
                    "supplier": "string",
                    "reason": "string",
                    "score": "number"
                }},
                "highest_quality": {{
                    "supplier": "string",
                    "reason": "string",
                    "score": "number"
                }},
                "recommendations": [
                    {{
                        "supplier": "string",
                        "reason": "string",
                        "pros": ["list"],
                        "cons": ["list"]
                    }}
                ],
                "risk_assessment": {{
                    "high_risk": ["list"],
                    "medium_risk": ["list"],
                    "low_risk": ["list"]
                }},
                "next_steps": ["list"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Provide comprehensive quote analysis."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                return {}
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            return json.loads(content.strip())
            
        except Exception as e:
            return {}

    async def _extract_order_info(self, user_message: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Extract order management information"""
        try:
            extraction_prompt = f"""
            Extract order management information from this conversation:
            
            User Message: {user_message}
            Conversation History: {json.dumps(conversation_history[-3:], indent=2)}
            
            Return in JSON format:
            {{
                "order_id": "string",
                "concern": "string",
                "status_request": "string",
                "action_needed": "string"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Extract order information accurately."},
                    {"role": "user", "content": extraction_prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                return {}
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            return json.loads(content.strip())
            
        except Exception as e:
            return {}

# Global instance
advanced_sourcing_agent = AdvancedSourcingAgent() 