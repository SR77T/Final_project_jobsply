from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.main.models import Category, Job, JobApplication, Contact
from datetime import datetime, timedelta

User = get_user_model()

class JobModelsTest(TestCase):
    def setUp(self):
        """Setup test data"""
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@example.com", 
            password="testpassword"
        )
        self.category = Category.objects.create(title="IT Jobs")
        self.job = Job.objects.create(
            title="Django Developer",
            company_name="TechCorp",
            description="Looking for a Django developer",
            location="New York",
            category=self.category,
            experience_required="2 years",
            salary=60000.00,
            apply_before=datetime.now() + timedelta(days=30),
        )
        self.application = JobApplication.objects.create(
            job=self.job,
            user=self.user,  # ✅ Use UUID instead of user object
            status="Applied",
            interview_date=datetime.now() + timedelta(days=10)
        )
        self.contact = Contact.objects.create(
            name="John Doe",
            company_name="TechCorp",
            email="johndoe@example.com",
            phone_number="1234567890",
            message="Interested in job opportunities"
        )

    def test_category_creation(self):
        """Test category creation"""
        self.assertEqual(self.category.title, "IT Jobs")

    def test_job_creation(self):
        """Test job creation"""
        self.assertEqual(self.job.title, "Django Developer")
        self.assertEqual(self.job.company_name, "TechCorp")
        self.assertEqual(self.job.category.title, "IT Jobs")

    def test_job_application_creation(self):
        """Test job application creation"""
        self.assertEqual(self.application.job.title, "Django Developer")
        self.assertEqual(self.application.user.email, "test@example.com")  # ✅ Now works correctly
        self.assertEqual(self.application.status, "Applied")

    def test_contact_creation(self):
        """Test contact form submission"""
        self.assertEqual(self.contact.name, "John Doe")
        self.assertEqual(self.contact.company_name, "TechCorp")
        self.assertEqual(self.contact.email, "johndoe@example.com")
