from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import BonusLevel, UserBonuses


class AuthTests(APITestCase):
    def setUp(self):
         self.username = "testuser"
         self.password = "testpassword"
         self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_successful(self):
         url = reverse('login')
         response = self.client.post(url, {'username': self.username, 'password': self.password})
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('message', response.data)

    def test_login_no_credentials(self):
         url = reverse('login')
         response = self.client.post(url, {})
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ModelTests(APITestCase):
    def test_bonus_level_creation(self):
        level = BonusLevel.objects.create(level_name='Алмазный', spending_threshold=5000, cashback_percentage=5)
        self.assertEqual(level.level_name, 'Алмазный')
        self.assertEqual(level.spending_threshold, 5000)
        self.assertEqual(level.cashback_percentage, 5)

    def test_user_bonuses_creation(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        level = BonusLevel.objects.create(level_name='Медный', spending_threshold=0, cashback_percentage=3)
        bonuses = UserBonuses.objects.create(user=user, current_spending=1000, level=level)
        self.assertEqual(bonuses.user, user)
        self.assertEqual(bonuses.current_spending, 1000)
        self.assertEqual(bonuses.level, level)