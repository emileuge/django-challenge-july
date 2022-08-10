from django.test import TestCase
from api.models import UserRequestHistory
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from rest_framework.response import Response
# Create your tests here.

class GetStockTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def login(self):
        self.user = User.objects.create(username='test', email='test@test.com')
        self.client.force_authenticate(user=self.user)
    
    def admin_login(self):
        self.user = User.objects.create(username='admin', email='admin@test.com', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    @patch('requests.get', spec_set=True)
    def get_stock(self, mock):
        self.login()
        data = {"symbol": "AAPL.US", "open": 161.24, "high": 163.63, "low": 159.5, "close": 162.51, "volume": 101786860, "name": "APPLE", "date": "2022-07-29 22:00:11"}
        mock().status_code = status.HTTP_200_OK
        mock().json = MagicMock(return_value=data)
        response = self.client.get('%s?q=%s' % (reverse('get-stock'), 'aapl.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(len(response), 8)
        self.assertEqual(response['name'], 'APPLE')
        self.assertEqual(UserRequestHistory.objects.all().count(), 1)
    
    def get_history(self):
        self.login()
        response = self.client.get('%s?q=%s' % (reverse('get-stock'), 'aapl.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('get-history'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(len(response), 1)

    def get_stats(self):
        self.login()

        response = self.client.get('%s?q=%s' % (reverse('get-stock'), 'aapl.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('%s?q=%s' % (reverse('get-stock'), 'aapl.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('%s?q=%s' % (reverse('get-stock'), 'aapl.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('%s?q=%s' % (reverse('get-stock'), 'msft.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('%s?q=%s' % (reverse('get-stock'), 'msft.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('get-stats'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin_login()
        response = self.client.get(reverse('get-stats'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(response[0]['stock'], 'AAPL.US')
        self.assertEqual(response[1]['stock'], 'MSFT.US')
