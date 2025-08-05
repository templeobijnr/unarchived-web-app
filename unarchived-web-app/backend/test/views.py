from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import tempfile
import base64
from typing import Dict, Any, List

# Import your app components
from users.models import User, UserProfile, UserPreferences
from dpgs.models import DigitalProductGenome, DPGComponent, ComponentSpecification, ApparelDPGExtension
from agentcore.agent import ConversationalAgent, create_agent
from projects.analysis import trigger_ai_analysis
from knowledge_base.models import KnowledgeChunk
from suppliers.models import Supplier
from rfq.models import RFQ
from quotes.models import Quote

@method_decorator(csrf_exempt, name='dispatch')
class TestingDashboardView(APIView):
    """Main testing dashboard endpoint"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Return testing dashboard data"""
        try:
            # Get basic stats
            stats = {
                'users_count': User.objects.count(),
                'dpgs_count': DigitalProductGenome.objects.count(),
                'suppliers_count': Supplier.objects.count(),
                'rfqs_count': RFQ.objects.count(),
                'quotes_count': Quote.objects.count(),
                'knowledge_chunks_count': KnowledgeChunk.objects.count(),
            }
            
            # Get recent items for testing
            recent_dpgs = list(DigitalProductGenome.objects.all()[:5].values('id', 'title', 'stage'))
            recent_users = list(User.objects.all()[:5].values('id', 'username', 'email'))
            
            return Response({
                'status': 'success',
                'stats': stats,
                'recent_dpgs': recent_dpgs,
                'recent_users': recent_users,
                'endpoints': {
                    'user_tests': '/test/users/',
                    'dpg_tests': '/test/dpgs/',
                    'agent_tests': '/test/agent/',
                    'analysis_tests': '/test/analysis/',
                    'knowledge_tests': '/test/knowledge/',
                    'supplier_tests': '/test/suppliers/',
                    'file_tests': '/test/files/',
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UserTestingView(APIView):
    """Test user management functionality"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def get(self, request):
        """Get all users for testing"""
        try:
            users = list(User.objects.all().values('id', 'username', 'email', 'is_verified'))
            return Response({'users': users})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def post(self, request):
        """Create test user"""
        try:
            data = request.data
            user = User.objects.create_user(
                username=data.get('username', f'test_user_{User.objects.count() + 1}'),
                email=data.get('email', f'test{User.objects.count() + 1}@example.com'),
                password=data.get('password', 'testpass123')
            )
            
            # Create profile
            UserProfile.objects.create(
                user=user,
                full_name=data.get('full_name', 'Test User'),
                bio=data.get('bio', 'Test user for testing purposes'),
                location=data.get('location', 'Test City')
            )
            
            # Create preferences
            UserPreferences.objects.create(
                user=user,
                receive_notifications=data.get('receive_notifications', True),
                dark_mode=data.get('dark_mode', False),
                language=data.get('language', 'en')
            )
            
            return Response({
                'status': 'success',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_verified': user.is_verified
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class DPGTestingView(APIView):
    """Test DPG functionality"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def get(self, request):
        """Get all DPGs for testing"""
        try:
            dpgs = list(DigitalProductGenome.objects.all().values(
                'id', 'title', 'description', 'stage', 'version', 'created_at'
            ))
            return Response({'dpgs': dpgs})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def post(self, request):
        """Create test DPG"""
        try:
            data = request.data
            
            # Get or create a test user
            user, created = User.objects.get_or_create(
                username='test_dpg_user',
                defaults={'email': 'dpg_test@example.com'}
            )
            
            dpg = DigitalProductGenome.objects.create(
                title=data.get('title', f'Test DPG {DigitalProductGenome.objects.count() + 1}'),
                description=data.get('description', 'Test DPG for testing purposes'),
                owner=user,
                version=data.get('version', '1.0'),
                stage=data.get('stage', 'created'),
                data=data.get('data', {'category': 'apparel', 'material': 'cotton'})
            )
            
            # Create test components
            component = DPGComponent.objects.create(
                name=data.get('component_name', 'Test Component'),
                description=data.get('component_description', 'Test component description'),
                dpg=dpg,
                order=1
            )
            
            ComponentSpecification.objects.create(
                component=component,
                material=data.get('material', 'cotton'),
                color=data.get('color', 'blue'),
                size=data.get('size', 'M'),
                quantity=data.get('quantity', 100),
                notes=data.get('notes', 'Test specification')
            )
            
            return Response({
                'status': 'success',
                'dpg': {
                    'id': dpg.id,
                    'title': dpg.title,
                    'description': dpg.description,
                    'stage': dpg.stage,
                    'version': dpg.version
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class AgentTestingView(APIView):
    """Test AI agent functionality"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def post(self, request):
        """Test agent conversation"""
        try:
            data = request.data
            message = data.get('message', 'Hello, I want to create a new product')
            dpg_id = data.get('dpg_id')
            
            # Create agent
            agent = create_agent(dpg_id=dpg_id)
            
            # Process message
            response = agent.chat(message)
            
            return Response({
                'status': 'success',
                'response': response,
                'suggestions': agent._generate_suggestions(agent.state)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class AnalysisTestingView(APIView):
    """Test AI analysis functionality"""
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, JSONParser]
    
    def post(self, request):
        """Test file analysis"""
        try:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({'error': 'No file uploaded'}, status=400)
            
            # Create a mock project file object
            class MockProjectFile:
                def __init__(self, file, filename):
                    self.file = file
                    self.original_filename = filename
                    self.file_type = 'text/plain'
                    self.project = MockProject()
            
            class MockProject:
                def __init__(self):
                    self.title = 'Test Project'
            
            project_file = MockProjectFile(uploaded_file, uploaded_file.name)
            
            # Trigger analysis
            trigger_ai_analysis(project_file)
            
            return Response({
                'status': 'success',
                'message': 'File analysis completed',
                'filename': uploaded_file.name
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class KnowledgeTestingView(APIView):
    """Test knowledge base functionality"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def get(self, request):
        """Get knowledge base stats"""
        try:
            chunks = list(KnowledgeChunk.objects.all().values('id', 'content', 'domain', 'entity_name')[:10])
            return Response({
                'chunks': chunks,
                'total_count': KnowledgeChunk.objects.count()
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def post(self, request):
        """Create test knowledge chunk"""
        try:
            data = request.data
            chunk = KnowledgeChunk.objects.create(
                content=data.get('content', 'Test knowledge content'),
                domain=data.get('domain', 'test'),
                entity_name=data.get('entity_name', 'test_entity'),
                source_document=data.get('source_document', 'test_doc'),
                source_type=data.get('source_type', 'test')
            )
            
            return Response({
                'status': 'success',
                'chunk': {
                    'id': chunk.id,
                    'content': chunk.content,
                    'domain': chunk.domain,
                    'entity_name': chunk.entity_name
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class FileTestingView(APIView):
    """Test file processing functionality"""
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]
    
    def post(self, request):
        """Test file upload and processing"""
        try:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({'error': 'No file uploaded'}, status=400)
            
            # Read file content
            content = uploaded_file.read().decode('utf-8', errors='ignore')
            
            return Response({
                'status': 'success',
                'filename': uploaded_file.name,
                'size': uploaded_file.size,
                'content_preview': content[:500] + '...' if len(content) > 500 else content
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SupplierTestingView(APIView):
    """Test supplier functionality"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def get(self, request):
        """Get all suppliers"""
        try:
            suppliers = list(Supplier.objects.all().values('id', 'name', 'email', 'specialization'))
            return Response({'suppliers': suppliers})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def post(self, request):
        """Create test supplier"""
        try:
            data = request.data
            supplier = Supplier.objects.create(
                name=data.get('name', f'Test Supplier {Supplier.objects.count() + 1}'),
                email=data.get('email', f'supplier{Supplier.objects.count() + 1}@example.com'),
                specialization=data.get('specialization', 'apparel'),
                contact_person=data.get('contact_person', 'Test Contact'),
                phone=data.get('phone', '+1234567890')
            )
            
            return Response({
                'status': 'success',
                'supplier': {
                    'id': supplier.id,
                    'name': supplier.name,
                    'email': supplier.email,
                    'specialization': supplier.specialization
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# Simple HTML dashboard view
def testing_dashboard_html(request):
    """HTML dashboard for testing"""
    return render(request, 'test/dashboard.html')