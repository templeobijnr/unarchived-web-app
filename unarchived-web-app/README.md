# Unarchived - AI-Powered Sourcing Platform

A full-stack application for managing supplier relationships, quotes, and RFQs built with Django (backend) and React (frontend).

## Project Structure

```
├── backend/          # Django backend
│   ├── core/         # Django project settings
│   ├── api/          # API app with models and views
│   ├── manage.py     # Django management script
│   └── venv/         # Python virtual environment
└── frontend/         # React frontend
    ├── src/          # Source code
    ├── package.json  # Dependencies
    └── vite.config.ts # Vite configuration
```

## Features

### Backend (Django)
- **Django REST Framework** for API endpoints
- **CORS support** for frontend communication
- **Authentication** with session-based auth
- **Models**: Suppliers, RFQs, Quotes, Messages, KPIs
- **Sample data** populated automatically

### Frontend (React)
- **TypeScript** for type safety
- **React Query** for data fetching
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Radix UI** components
- **Real-time data** from Django API

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Populate sample data:**
   ```bash
   python manage.py populate_sample_data
   ```

6. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

The Django backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

The React frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /admin/login/` - Login
- `POST /admin/logout/` - Logout

### Suppliers
- `GET /api/suppliers/` - List suppliers
- `GET /api/suppliers/{id}/` - Get supplier details
- `POST /api/suppliers/` - Create supplier
- `PUT /api/suppliers/{id}/` - Update supplier
- `DELETE /api/suppliers/{id}/` - Delete supplier

### RFQs
- `GET /api/rfqs/` - List RFQs
- `GET /api/rfqs/{id}/` - Get RFQ details
- `POST /api/rfqs/` - Create RFQ
- `PUT /api/rfqs/{id}/` - Update RFQ
- `DELETE /api/rfqs/{id}/` - Delete RFQ

### Quotes
- `GET /api/quotes/` - List quotes
- `GET /api/quotes/{id}/` - Get quote details
- `POST /api/quotes/` - Create quote
- `PUT /api/quotes/{id}/` - Update quote
- `DELETE /api/quotes/{id}/` - Delete quote

### Dashboard
- `GET /api/dashboard/kpis/` - Get KPI data
- `GET /api/dashboard/recent_activity/` - Get recent activity
- `GET /api/dashboard/upcoming_deadlines/` - Get upcoming deadlines

## Database Models

### Supplier
- Basic info (name, logo, category, region)
- Reliability score
- Capabilities and certifications
- Contact information

### RFQ (Request for Quote)
- Title, description, category
- Quantity and target price
- Deadline and status
- Created by user

### Quote
- Links to RFQ and supplier
- Price, currency, lead time
- Status (pending, accepted, rejected, expired)
- Product specifications

### Message
- Chat messages between user and AI
- Author (user/ai)
- Content and timestamp

### KPI
- Key performance indicators
- Cost savings, quotes in flight
- On-time rate, lead times

## Authentication

The application uses Django's built-in authentication system:

- **Default admin user**: `admin` / `admin123`
- **Session-based authentication** for API access
- **CORS configured** for frontend communication

## Development

### Backend Development

1. **Create new Django app:**
   ```bash
   python manage.py startapp myapp
   ```

2. **Add to INSTALLED_APPS in settings.py**

3. **Create models and run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create API views and serializers**

### Frontend Development

1. **Add new API endpoints** in `src/lib/api.ts`

2. **Create new components** in `src/components/`

3. **Add new pages** in `src/pages/`

4. **Update routing** in `src/App.tsx`

## Environment Variables

### Backend
Create a `.env` file in the backend directory:
```
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=unarchived_db
DB_USER=unarchived_user
DB_PASSWORD=unarchived_pass
DB_HOST=localhost
DB_PORT=5432
```

### Frontend
The frontend uses environment variables for API configuration. Create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:8000
```

## Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure production database
3. Set up static file serving
4. Use production WSGI server (Gunicorn)

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve static files from a web server
3. Configure API URL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 