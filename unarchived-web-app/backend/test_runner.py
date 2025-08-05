#!/usr/bin/env python3
"""
Test Runner for Unarchived Web App
This script helps you start the testing interface and provides instructions.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_django_setup():
    """Check if Django is properly set up"""
    try:
        import django
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()
        
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def check_database():
    """Check database connection and migrations"""
    try:
        from django.core.management import execute_from_command_line
        
        # Run migrations
        print("🔄 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Database setup successful")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def start_server():
    """Start the Django development server"""
    try:
        print("🚀 Starting Django development server...")
        print("📝 The testing interface will be available at: http://localhost:8000/test/html/")
        print("🔧 API endpoints will be available at: http://localhost:8000/test/")
        print("\n" + "="*60)
        print("🧪 TESTING DASHBOARD INSTRUCTIONS")
        print("="*60)
        print("1. Open your browser and go to: http://localhost:8000/test/html/")
        print("2. You'll see a beautiful testing interface with sections for:")
        print("   - 👤 User Management (create/test users)")
        print("   - 🧬 Digital Product Genomes (create/test DPGs)")
        print("   - 🤖 AI Agent (test conversational AI)")
        print("   - 📄 File Analysis (upload and analyze files)")
        print("   - 🧠 Knowledge Base (add/retrieve knowledge)")
        print("   - 🏭 Suppliers (create/test suppliers)")
        print("3. Each section has forms to create test data and buttons to load existing data")
        print("4. The interface shows real-time stats and provides detailed responses")
        print("5. You can test all your app components without writing any code!")
        print("\n" + "="*60)
        print("🎯 QUICK START:")
        print("1. Try creating a test user first")
        print("2. Then create a DPG (Digital Product Genome)")
        print("3. Test the AI agent with a message like 'I want to create a new product'")
        print("4. Upload a file to test the analysis functionality")
        print("5. Add some knowledge to the knowledge base")
        print("6. Create a test supplier")
        print("\n" + "="*60)
        
        # Start the server
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main function"""
    print("🧪 Unarchived Web App - Testing Interface")
    print("="*50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the Django project root.")
        return
    
    # Check Django setup
    if not check_django_setup():
        print("❌ Please fix Django setup issues before continuing.")
        return
    
    # Check database
    if not check_database():
        print("❌ Please fix database issues before continuing.")
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 