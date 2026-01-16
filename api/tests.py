from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Employee
from datetime import date


class EmployeeAPITestCase(TestCase):
    """Test suite for Employee API endpoints"""
    
    def setUp(self):
        """Set up test client and create test user for authentication"""
        self.client = APIClient()
        
        # Create a test user for JWT authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Get JWT token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        
        # Set authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create sample employees for testing
        self.employee1 = Employee.objects.create(
            name='John Doe',
            email='john@example.com',
            department='Engineering',
            role='Developer'
        )
        
        self.employee2 = Employee.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            department='HR',
            role='Manager'
        )
        
    def tearDown(self):
        """Clean up after each test"""
        Employee.objects.all().delete()
        User.objects.all().delete()


class EmployeeListCreateTests(EmployeeAPITestCase):
    """Test cases for listing and creating employees"""
    
    def test_list_employees_success(self):
        """Test retrieving list of all employees"""
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('results', response.data)
        
    def test_list_employees_without_authentication(self):
        """Test that unauthenticated requests are rejected"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_employee_success(self):
        """Test creating a new employee with valid data"""
        data = {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'department': 'Sales',
            'role': 'Analyst'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 3)
        self.assertEqual(response.data['name'], 'Alice Johnson')
        self.assertEqual(response.data['email'], 'alice@example.com')
        
    def test_create_employee_duplicate_email(self):
        """Test that duplicate email addresses are rejected"""
        data = {
            'name': 'John Duplicate',
            'email': 'john@example.com',  # Already exists
            'department': 'Engineering',
            'role': 'Developer'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
    def test_create_employee_missing_name(self):
        """Test that name field is required"""
        data = {
            'email': 'test@example.com',
            'department': 'Engineering'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        
    def test_create_employee_missing_email(self):
        """Test that email field is required"""
        data = {
            'name': 'Test User',
            'department': 'Engineering'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
    def test_create_employee_invalid_email(self):
        """Test that invalid email format is rejected"""
        data = {
            'name': 'Test User',
            'email': 'invalid-email',
            'department': 'Engineering'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
    def test_create_employee_empty_name(self):
        """Test that empty name is rejected"""
        data = {
            'name': '',
            'email': 'test@example.com',
            'department': 'Engineering'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        
    def test_create_employee_with_optional_fields_empty(self):
        """Test creating employee without department and role (optional fields)"""
        data = {
            'name': 'Bob Williams',
            'email': 'bob@example.com'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['department'], '')
        self.assertEqual(response.data['role'], '')
        
    def test_create_employee_invalid_department(self):
        """Test that invalid department choice is rejected"""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'department': 'InvalidDepartment'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('department', response.data)
        
    def test_create_employee_invalid_role(self):
        """Test that invalid role choice is rejected"""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'role': 'InvalidRole'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('role', response.data)


class EmployeeDetailTests(EmployeeAPITestCase):
    """Test cases for retrieving, updating, and deleting individual employees"""
    
    def test_retrieve_employee_success(self):
        """Test retrieving a single employee by ID"""
        response = self.client.get(f'/api/employees/{self.employee1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.data['email'], 'john@example.com')
        
    def test_retrieve_employee_not_found(self):
        """Test retrieving non-existent employee returns 404"""
        response = self.client.get('/api/employees/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_employee_success(self):
        """Test updating employee with PUT"""
        data = {
            'name': 'John Updated',
            'email': 'john@example.com',
            'department': 'Sales',
            'role': 'Manager'
        }
        response = self.client.put(f'/api/employees/{self.employee1.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.name, 'John Updated')
        self.assertEqual(self.employee1.department, 'Sales')
        self.assertEqual(self.employee1.role, 'Manager')
        
    def test_partial_update_employee_success(self):
        """Test updating employee with PATCH"""
        data = {
            'department': 'HR'
        }
        response = self.client.patch(f'/api/employees/{self.employee1.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.department, 'HR')
        self.assertEqual(self.employee1.name, 'John Doe')  # Unchanged
        
    def test_update_employee_duplicate_email(self):
        """Test that updating to duplicate email is rejected"""
        data = {
            'name': 'John Doe',
            'email': 'jane@example.com',  # employee2's email
            'department': 'Engineering',
            'role': 'Developer'
        }
        response = self.client.put(f'/api/employees/{self.employee1.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
    def test_delete_employee_success(self):
        """Test deleting an employee"""
        response = self.client.delete(f'/api/employees/{self.employee1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertFalse(Employee.objects.filter(id=self.employee1.id).exists())
        
    def test_delete_employee_not_found(self):
        """Test deleting non-existent employee returns 404"""
        response = self.client.delete('/api/employees/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeeFilterTests(EmployeeAPITestCase):
    """Test cases for filtering employees"""
    
    def setUp(self):
        super().setUp()
        # Create additional employees for filtering tests
        Employee.objects.create(
            name='Alice Engineer',
            email='alice.eng@example.com',
            department='Engineering',
            role='Developer'
        )
        Employee.objects.create(
            name='Bob Manager',
            email='bob.mgr@example.com',
            department='Engineering',
            role='Manager'
        )
        
    def test_filter_by_department(self):
        """Test filtering employees by department"""
        response = self.client.get('/api/employees/?department=Engineering')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)  # John, Alice, Bob
        
    def test_filter_by_role(self):
        """Test filtering employees by role"""
        response = self.client.get('/api/employees/?role=Developer')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # John, Alice
        
    def test_filter_by_department_and_role(self):
        """Test filtering employees by both department and role"""
        response = self.client.get('/api/employees/?department=Engineering&role=Manager')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Only Bob
        
    def test_filter_no_results(self):
        """Test filtering with no matching results"""
        response = self.client.get('/api/employees/?department=Sales&role=Developer')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


class EmployeePaginationTests(EmployeeAPITestCase):
    """Test cases for pagination"""
    
    def setUp(self):
        super().setUp()
        # Create 15 employees to test pagination (PAGE_SIZE is 10)
        for i in range(13):
            Employee.objects.create(
                name=f'Employee {i}',
                email=f'employee{i}@example.com',
                department='Engineering',
                role='Developer'
            )
            
    def test_pagination_first_page(self):
        """Test first page of results"""
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['count'], 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        
    def test_pagination_second_page(self):
        """Test second page of results"""
        response = self.client.get('/api/employees/?page=2')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
        
    def test_pagination_invalid_page(self):
        """Test requesting invalid page number"""
        response = self.client.get('/api/employees/?page=999')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class JWTAuthenticationTests(TestCase):
    """Test cases for JWT authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_obtain_token_success(self):
        """Test obtaining JWT token with valid credentials"""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_obtain_token_invalid_credentials(self):
        """Test that invalid credentials are rejected"""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_refresh_token_success(self):
        """Test refreshing JWT token"""
        # First obtain tokens
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        refresh_token = response.data['refresh']
        
        # Refresh the token
        response = self.client.post('/api/token/refresh/', {
            'refresh': refresh_token
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    def test_verify_token_success(self):
        """Test verifying valid JWT token"""
        # Obtain token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        access_token = response.data['access']
        
        # Verify token
        response = self.client.post('/api/token/verify/', {
            'token': access_token
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_verify_token_invalid(self):
        """Test that invalid token is rejected"""
        response = self.client.post('/api/token/verify/', {
            'token': 'invalid_token'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeModelTests(TestCase):
    """Test cases for Employee model"""
    
    def test_employee_creation(self):
        """Test creating an employee instance"""
        employee = Employee.objects.create(
            name='Test Employee',
            email='test@example.com',
            department='Engineering',
            role='Developer'
        )
        
        self.assertEqual(str(employee), 'Test Employee')
        self.assertEqual(employee.name, 'Test Employee')
        self.assertEqual(employee.email, 'test@example.com')
        self.assertIsInstance(employee.date_joined, date)
        
    def test_employee_string_representation(self):
        """Test __str__ method returns employee name"""
        employee = Employee.objects.create(
            name='John Doe',
            email='john@example.com'
        )
        
        self.assertEqual(str(employee), 'John Doe')
        
    def test_date_joined_auto_set(self):
        """Test that date_joined is automatically set"""
        employee = Employee.objects.create(
            name='Test Employee',
            email='test@example.com'
        )
        
        self.assertIsNotNone(employee.date_joined)
        self.assertEqual(employee.date_joined, date.today())