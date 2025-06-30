#!/usr/bin/env python3
"""
Demo script for the AI Sourcing Agent
Shows the complete "Pay and Wait" vision in action
"""

import os
import sys
import django
from dotenv import load_dotenv

# Add backend to Python path
sys.path.append('backend')

# Load environment variables
load_dotenv('backend/env')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.ai_agent import sourcing_agent

def demo_conversation():
    """Demo a complete sourcing conversation"""
    print("🤖 AI Sourcing Agent Demo")
    print("=" * 50)
    print("This demo shows how the AI handles a complete sourcing request")
    print("from initial inquiry to supplier recommendations.\n")
    
    # Simulate a conversation
    conversation = []
    
    # User's initial request
    user_message = "I need 10,000 custom phone cases with my company logo"
    print(f"👤 User: {user_message}")
    
    # AI response
    ai_response = sourcing_agent.get_response(user_message, conversation)
    print(f"🤖 AI: {ai_response}")
    conversation.append({"author": "user", "content": user_message})
    conversation.append({"author": "ai", "content": ai_response})
    
    print("\n" + "-" * 50)
    
    # User provides more details
    user_message = "I need them for iPhone 15, made of silicone, with my logo printed on the back. Target price around $2 per unit, and I need them in 30 days."
    print(f"👤 User: {user_message}")
    
    # AI response with RFQ creation
    ai_response = sourcing_agent.get_response(user_message, conversation)
    print(f"🤖 AI: {ai_response}")
    conversation.append({"author": "user", "content": user_message})
    conversation.append({"author": "ai", "content": ai_response})
    
    print("\n" + "-" * 50)
    
    # Extract RFQ details
    print("📋 Creating RFQ from conversation...")
    rfq_data = sourcing_agent.create_rfq_from_conversation(user_message, conversation)
    print(f"✅ RFQ Data: {rfq_data}")
    
    print("\n" + "-" * 50)
    
    # Get supplier suggestions
    print("🏭 Finding suppliers...")
    suppliers = sourcing_agent.suggest_suppliers("phone cases", "silicone, custom printing, iPhone 15")
    print("✅ Supplier Suggestions:")
    for supplier in suppliers:
        print(f"   • {supplier['name']} ({supplier['region']}) - {supplier['reliability']}% reliability")
        print(f"     Reason: {supplier['reason']}")
    
    print("\n" + "=" * 50)
    print("🎯 This demonstrates the foundation of the 'Pay and Wait' vision!")
    print("The AI can now:")
    print("✅ Understand product requirements from natural language")
    print("✅ Extract detailed specifications")
    print("✅ Create structured RFQs")
    print("✅ Find relevant suppliers")
    print("✅ Provide intelligent recommendations")
    print("\nNext steps: Add order management, quality control, and logistics!")

def demo_advanced_features():
    """Demo advanced AI features"""
    print("\n🚀 Advanced AI Features Demo")
    print("=" * 50)
    
    # Test different types of requests
    requests = [
        "I need 5,000 wireless earbuds with custom branding",
        "Looking for suppliers of organic cotton t-shirts, 20,000 units",
        "Need custom packaging for my skincare products",
        "Sourcing LED strip lights for home automation project"
    ]
    
    for request in requests:
        print(f"\n👤 User: {request}")
        response = sourcing_agent.get_response(request)
        print(f"🤖 AI: {response[:200]}...")
        print("-" * 30)

if __name__ == "__main__":
    print("🎉 AI Sourcing Agent - Complete Demo")
    print("=" * 60)
    
    # Run the main demo
    demo_conversation()
    
    # Run advanced features demo
    demo_advanced_features()
    
    print("\n" + "=" * 60)
    print("🎯 Ready to build the world-class AI sourcing agent!")
    print("Your foundation is solid - let's add the automation layers!") 