#!/usr/bin/env python3
"""
Simple test script for the AI sourcing agent
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv('env')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from agentcore.ai_agent import sourcing_agent

def test_ai_response():
    """Test basic AI response functionality"""
    print("🤖 Testing AI Sourcing Agent...")
    
    # Test basic response
    user_message = "I need to source 10,000 custom phone cases with my company logo"
    
    try:
        response = sourcing_agent.get_response(user_message)
        print(f"✅ AI Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_rfq_extraction():
    """Test RFQ extraction from conversation"""
    print("\n📋 Testing RFQ Extraction...")
    
    conversation_history = [
        {"author": "user", "content": "I need phone cases", "timestamp": "2024-01-01T10:00:00Z"},
        {"author": "ai", "content": "I can help you source phone cases. What quantity do you need?", "timestamp": "2024-01-01T10:01:00Z"},
        {"author": "user", "content": "About 10,000 units", "timestamp": "2024-01-01T10:02:00Z"}
    ]
    
    current_message = "I need custom phone cases with my logo, target price around $2 per unit"
    
    try:
        rfq_data = sourcing_agent.create_rfq_from_conversation(current_message, conversation_history)
        print(f"✅ RFQ Data: {rfq_data}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_supplier_suggestions():
    """Test supplier suggestion functionality"""
    print("\n🏭 Testing Supplier Suggestions...")
    
    try:
        suggestions = sourcing_agent.suggest_suppliers("phone cases", "custom printing, logo")
        print(f"✅ Supplier Suggestions: {suggestions}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting AI Agent Tests...\n")
    
    # Run tests
    test1 = test_ai_response()
    test2 = test_rfq_extraction()
    test3 = test_supplier_suggestions()
    
    print(f"\n📊 Test Results:")
    print(f"Basic AI Response: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"RFQ Extraction: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Supplier Suggestions: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All tests passed! AI agent is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.") 