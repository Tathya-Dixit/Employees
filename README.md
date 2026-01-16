# Employee Management API

A RESTful API built with Django and Django REST Framework for managing employee records with JWT authentication.

## Features
- 🔐 JWT-based authentication
- 👥 Complete CRUD operations for employees
- 🔍 Filter by department and role
- 📄 Pagination support
- ✅ Comprehensive test coverage
- 🚀 Production-ready deployment

## Tech Stack
- Django 6.0.1
- Django REST Framework 3.16.1
- PostgreSQL (Production) / SQLite (Development)
- JWT Authentication

## Project Setup

1. Clone the repo:
```sh
git clone https://github.com/Tathya-Dixit/Employees
cd Employees
```

2. Create & activate virtual environment:
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```sh
python manage.py migrate
```

6. Create a superuser:
```sh
python manage.py createsuperuser
```

7. Run the development server:
```sh
python manage.py runserver
```

Access the API at: http://127.0.0.1:8000/api/employees/  
Admin panel: http://127.0.0.1:8000/admin/

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

### Employees
- `GET /api/employees/` - List all employees (supports filtering & pagination)
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Retrieve employee details
- `PUT /api/employees/{id}/` - Update employee
- `PATCH /api/employees/{id}/` - Partial update employee
- `DELETE /api/employees/{id}/` - Delete employee

### Query Parameters
- `?department=Engineering` - Filter by department
- `?role=Developer` - Filter by role
- `?page=2` - Pagination

## Usage Example

1. Obtain JWT token:
```sh
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

2. Create employee:
```sh
curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "department": "Engineering",
    "role": "Developer"
  }'
```

3. List employees:
```sh
curl -X GET http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Running Tests

```sh
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

The app is configured for deployment on Render.com:

1. Push your code to GitHub
2. Connect repository to Render
3. Add environment variables in Render dashboard
4. Deploy!

Live Demo: [https://employees-ren6.onrender.com]
