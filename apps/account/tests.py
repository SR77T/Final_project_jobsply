from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import UserProfile, UserAccountActivation
from django.core.exceptions import ValidationError
from django.urls import reverse


User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        """Create a sample user for testing"""
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User"
        )

    def test_user_creation(self):
        """Ensure user instance is created properly"""
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("securepassword123"))
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        """Ensure superuser creation works properly"""
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_email_unique_constraint(self):
        """Ensure duplicate emails raise an error"""
        with self.assertRaises(Exception):  
            User.objects.create_user(email="testuser@example.com", password="newpassword")

class UserProfileTest(TestCase):
    def setUp(self):
        """Create a user and profile"""
        self.user = User.objects.create_user(email="profileuser@example.com", password="testpassword")
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number="+1234567890",
            address="123 Test Street",
            bio="This is a test bio."
        )

    def test_profile_creation(self):
        """Ensure profile is linked to user"""
        self.assertEqual(self.profile.user.email, "profileuser@example.com")
        self.assertEqual(self.profile.phone_number, "+1234567890")

class UserAccountActivationTest(TestCase):
    def setUp(self):
        """Create an activation instance"""
        self.activation = UserAccountActivation.objects.create(email="activation@example.com", key="activationkey123")

    def test_activation_creation(self):
        """Ensure activation entry is created"""
        self.assertEqual(self.activation.email, "activation@example.com")
        self.assertEqual(self.activation.key, "activationkey123")


# class UserViewTest(TestCase):
#     def setUp(self):
#         """Set up a test user and client"""
#         self.client = Client()
#         self.user = User.objects.create_user(email="testlogin@example.com", password="testpassword")

#     def test_register_view(self):
#         """Test user registration"""
#         response = self.client.post(reverse("user_register"), {
#             "email": "newuser@example.com",
#             "password": "newpassword",
#             "confirm_password": "newpassword",
#             "first_name": "New",
#             "last_name": "User"
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after successful registration
#         self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

#     def test_login_view(self):
#         """Test user login"""
#         response = self.client.post(reverse("user_login"), {
#             "email": "testlogin@example.com",
#             "password": "testpassword"
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after login
#         self.assertIn("_auth_user_id", self.client.session)  # Ensure user is authenticated

#     def test_login_invalid_credentials(self):
#         """Ensure login fails for incorrect credentials"""
#         response = self.client.post(reverse("user_login"), {
#             "email": "testlogin@example.com",
#             "password": "wrongpassword"
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertNotIn("_auth_user_id", self.client.session)  # User should not be logged in

#     def test_logout_view(self):
#         """Test user logout functionality"""
#         self.client.login(email="testlogin@example.com", password="testpassword")
#         response = self.client.get(reverse("user_Logout"))
#         self.assertEqual(response.status_code, 302)  # Redirect after logout
#         self.assertNotIn("_auth_user_id", self.client.session)  # Ensure user is logged out   