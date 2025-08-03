from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.core.management import call_command

User = get_user_model()

class UserRegistrationFlowTests(APITestCase):
    def setUp(self):
        # Ensure all migrations applied in test DB
        call_command('migrate', verbosity=0)

        self.register_url = '/api/users/auth/register/'
        self.login_url = '/api/users/auth/login/'
        self.token_url = '/api/users/token/'

    def test_register_and_verify_email(self):
        # Step 1: Register user
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'SecurePass123!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_verified)

        # Step 2: Verify email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = reverse('users:activate', kwargs={'uidb64': uid, 'token': token})
        response = self.client.get(verify_url)
        self.assertEqual(response.status_code, 200)
        print("Response Data:", response.data)
        user.refresh_from_db()
        self.assertTrue(user.is_verified)

    def test_login_fails_if_not_verified(self):
        user = User.objects.create_user(username='noverify', email='noverify@example.com', password='NoPass123')
        user.is_verified = False
        user.save()

        response = self.client.post(self.token_url, {
            'username': 'noverify@example.com',
            'password': 'NoPass123'
        })
        print("Response Data:", response.data["non_field_errors"])
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email is not verified",  response.data["non_field_errors"])

    def test_login_succeeds_if_verified(self):
        user = User.objects.create_user(username='yesverify', email='yesverify@example.com', password='YesPass123')
        user.is_verified = True
        user.save()

        self.assertTrue(User.objects.filter(email='yesverify@example.com').exists())

        response = self.client.post(self.login_url, {
            'username': 'yesverify@example.com',
            'password': 'YesPass123'
        })

        print("Response Data:", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_resend_verification_email(self):
        
        user = User.objects.create_user(username='resendme', email='resend@example.com', password='resend123')
        user.is_verified = False
        user.save()

        response = self.client.post(('/api/users/auth/resend_verification/'), {
            'email': 'resend@example.com'
        })
        self.assertEqual(response.status_code, 200)

