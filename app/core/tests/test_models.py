from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """"Testing core models"""

    def test_create_user_successful(self):
        """Test creating user with email and password successul"""
        email = 'admin@example.com'
        password = 'Admin@password'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(password, user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test that new user email is normalised before creation"""

        email = 'testmail@TEK.com'
        password = 'test@password'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_invalid_email(self):
        """test new user creation invalid emaill"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                password='test@123'
            )

    def test_create_new_superuser(self):
        """"Test Creating new superuser successful"""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test@password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)