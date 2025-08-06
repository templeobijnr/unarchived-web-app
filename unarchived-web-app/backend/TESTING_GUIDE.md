# 🧪 Unarchived Web App - Testing Guide

## Overview

This testing interface provides a comprehensive way to test all components of your Unarchived Web App without writing any code. It includes a beautiful, modern UI that allows you to interact with all the major system components.

## 🚀 Quick Start

### Option 1: Using the Test Runner (Recommended)
```bash
python test_runner.py
```

### Option 2: Manual Start
```bash
python manage.py runserver
```

Then open your browser and go to: **http://localhost:8000/test/html/**

## 📊 Dashboard Overview

The testing dashboard provides:

1. **Real-time Statistics** - Shows counts of users, DPGs, suppliers, RFQs, quotes, and knowledge chunks
2. **Interactive Testing Sections** - Six main testing areas for different components
3. **Live Results** - Immediate feedback on all operations
4. **Beautiful UI** - Modern, responsive design with drag-and-drop file uploads

## 🧪 Testing Sections

### 1. 👤 User Management
**Purpose**: Test user creation, profiles, and preferences

**Features**:
- Create test users with custom data
- Automatically creates user profiles and preferences
- Load existing users
- Test user verification system

**Test Scenarios**:
- Create users with different roles
- Test profile management
- Verify user preferences work correctly

### 2. 🧬 Digital Product Genome (DPG)
**Purpose**: Test the core product specification system

**Features**:
- Create DPGs with components and specifications
- Test different lifecycle stages (created, reviewed, approved, used)
- Add component specifications with materials, colors, sizes
- Load existing DPGs

**Test Scenarios**:
- Create apparel DPGs with fabric specifications
- Test DPG lifecycle progression
- Verify component relationships
- Test apparel-specific extensions

### 3. 📋 Project Management
**Purpose**: Test the comprehensive project management system

**Features**:
- Create projects with stages, status, and categories
- Manage project members with different roles (Owner, Editor, Viewer)
- Create and manage project stages
- Update project context (design intent, business requirements)
- Handle project file uploads with AI analysis

**Test Scenarios**:
- Create projects with different statuses and stages
- Add team members with various roles
- Test project context engine updates
- Upload files and test AI analysis integration
- Verify project-DPG relationships

### 4. 🤖 AI Agent
**Purpose**: Test the conversational AI system

**Features**:
- Send messages to the AI agent
- Test with existing DPGs or start new conversations
- Get AI responses and suggestions
- Test the agent's decision-making capabilities

**Test Scenarios**:
- Ask about creating new products
- Request DPG modifications
- Test knowledge retrieval
- Verify agent suggestions

### 5. 📄 File Analysis
**Purpose**: Test document processing and AI analysis

**Features**:
- Upload various file types (PDF, DOC, TXT, etc.)
- Drag-and-drop file upload
- Test OCR and text extraction
- Trigger AI analysis on uploaded files

**Test Scenarios**:
- Upload product specifications
- Test document parsing
- Verify AI analysis results
- Test different file formats

### 6. 🧠 Knowledge Base
**Purpose**: Test the vector-based knowledge system

**Features**:
- Add knowledge chunks with domains and entities
- Test knowledge retrieval
- Load existing knowledge
- Test domain-specific searches

**Test Scenarios**:
- Add material specifications
- Test knowledge retrieval by domain
- Verify entity relationships
- Test knowledge chunk creation

### 7. 🏭 Suppliers
**Purpose**: Test supplier management system

**Features**:
- Create test suppliers with specializations
- Load existing suppliers
- Test supplier categorization
- Verify contact information

**Test Scenarios**:
- Create suppliers for different categories
- Test supplier specialization matching
- Verify contact management
- Test supplier-DPG relationships

## 🔧 API Endpoints

The testing interface also provides REST API endpoints for programmatic testing:

- `GET /test/` - Dashboard statistics
- `GET/POST /test/users/` - User management
- `GET/POST /test/dpgs/` - DPG management
- `GET/POST /test/projects/` - Project management
- `GET/POST /test/project-members/` - Project member management
- `GET/POST /test/project-stages/` - Project stage management
- `GET/POST /test/project-context/` - Project context engine
- `GET/POST /test/project-uploads/` - Project file uploads
- `POST /test/agent/` - AI agent testing
- `POST /test/analysis/` - File analysis
- `GET/POST /test/knowledge/` - Knowledge base
- `GET/POST /test/suppliers/` - Supplier management
- `POST /test/files/` - File processing

## 🎯 Testing Workflows

### Basic Product Creation Workflow
1. **Create a User** - Start with a test user
2. **Create a Project** - Set up project structure and context
3. **Add Project Members** - Add team members with roles
4. **Create a DPG** - Define product specifications
5. **Add Knowledge** - Add relevant material/process knowledge
6. **Test AI Agent** - Ask the agent about the product
7. **Upload Files** - Add supporting documents
8. **Create Suppliers** - Add potential suppliers

### Advanced Testing Scenarios

#### Scenario 1: Apparel Product Development
1. Create user with apparel expertise
2. Create project for "Summer Collection 2024"
3. Add team members (designer, product manager)
4. Create DPG for "Cotton T-Shirt"
5. Add fabric composition knowledge
6. Test AI agent with "What materials should I use?"
7. Upload design specifications
8. Create textile suppliers

#### Scenario 2: Supplier Discovery
1. Create project for "Supplier Evaluation"
2. Create multiple suppliers with different specializations
3. Create DPG with specific requirements
4. Use AI agent to find matching suppliers
5. Test RFQ generation
6. Verify supplier matching logic

#### Scenario 3: Knowledge Integration
1. Create project for "Knowledge Base Development"
2. Add comprehensive material knowledge
3. Create DPGs that reference this knowledge
4. Test AI agent's knowledge retrieval
5. Verify knowledge chunk relationships
6. Test domain-specific searches

## 🐛 Troubleshooting

### Common Issues

1. **Database Errors**
   - Run `python manage.py migrate`
   - Check database connection settings

2. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path and virtual environment

3. **File Upload Issues**
   - Check file permissions
   - Verify file size limits
   - Ensure supported file types

4. **AI Agent Errors**
   - Check OpenAI API key configuration
   - Verify internet connection
   - Check API rate limits

### Debug Mode

To enable debug mode, set `DEBUG = True` in your Django settings and check the console output for detailed error messages.

## 📈 Performance Testing

The testing interface can also be used for performance testing:

1. **Load Testing**: Create multiple users, DPGs, and suppliers
2. **File Processing**: Upload large files to test processing speed
3. **AI Response Time**: Test agent response times with various queries
4. **Database Performance**: Monitor query performance with large datasets

## 🔒 Security Testing

Test security features:

1. **Authentication**: Test user creation and verification
2. **Authorization**: Verify proper access controls
3. **Input Validation**: Test form validation and sanitization
4. **File Security**: Test file upload restrictions

## 📝 Best Practices

1. **Start Small**: Begin with basic functionality before complex workflows
2. **Test Incrementally**: Test one component at a time
3. **Document Issues**: Note any problems for later resolution
4. **Clean Up**: Remove test data when done (or use separate test database)
5. **Version Control**: Keep track of test scenarios and results

## 🎉 Success Indicators

Your testing is successful when:

- ✅ All forms submit without errors
- ✅ AI agent provides relevant responses
- ✅ File uploads process correctly
- ✅ Knowledge base retrieves appropriate information
- ✅ DPGs create with proper relationships
- ✅ Suppliers match with relevant specializations
- ✅ Real-time stats update correctly

## 🚀 Next Steps

After successful testing:

1. **Production Deployment**: Deploy tested components to production
2. **User Training**: Train users on the new features
3. **Monitoring**: Set up monitoring for production systems
4. **Feedback Loop**: Collect user feedback for improvements

---

**Happy Testing! 🧪✨**

For support or questions, check the project documentation or create an issue in the repository. 