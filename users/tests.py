from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import UserActivity

class UserActivityTrackingTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user_data = {'username': 'testuser', 'password': 'testpassword123'}
        User.objects.filter(username=self.user_data['username']).delete() # Ensure clean state
        self.user = User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])

        self.admin_data = {'username': 'adminuser', 'password': 'adminpassword123'}
        User.objects.filter(username=self.admin_data['username']).delete() # Ensure clean state
        self.admin_user = User.objects.create_superuser(username=self.admin_data['username'], password=self.admin_data['password'])
        
        self.login_url = reverse('users-login') 
        self.activities_url = reverse('useractivities-list')

    def test_activity_created_on_login(self):
        UserActivity.objects.filter(user=self.user).delete()
        self.assertEqual(UserActivity.objects.filter(user=self.user).count(), 0)

        response = self.client.post(self.login_url, self.user_data, format='json')
        # Add detailed assertion message
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Login failed: {response.data}")
        
        self.assertEqual(UserActivity.objects.filter(user=self.user).count(), 1)
        activity = UserActivity.objects.filter(user=self.user).first()
        self.assertIsNotNone(activity)
        if activity: # Check to prevent AttributeError if activity is None
            self.assertEqual(activity.user, self.user)
            self.assertEqual(activity.action, "login")

    def test_admin_can_access_activities(self):
        login_response = self.client.post(self.login_url, self.admin_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, f"Admin login failed: {login_response.data}")
        token = login_response.data['token']
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        UserActivity.objects.create(user=self.admin_user, action="test_action_by_admin")
        UserActivity.objects.create(user=self.user, action="test_action_by_user")

        response = self.client.get(self.activities_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Accessing activities as admin failed: {response.data}")
        
        self.assertGreaterEqual(len(response.data), 2) 
        
        actions_in_response = [item['action'] for item in response.data]
        users_in_response = [item['user'] for item in response.data]

        self.assertIn("test_action_by_admin", actions_in_response)
        self.assertIn(self.admin_user.id, users_in_response)

        self.assertIn("test_action_by_user", actions_in_response)
        self.assertIn(self.user.id, users_in_response)


    def test_non_admin_cannot_access_activities(self):
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, f"User login failed: {login_response.data}")
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        response = self.client.get(self.activities_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, f"Non-admin access not forbidden: {response.data}")
