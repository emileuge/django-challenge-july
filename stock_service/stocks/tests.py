from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from django.http import JsonResponse

# Create your tests here.
class GetStockServiceTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('requests.get', spec_set=True)
    def get_stock_service(self, mock_get):
        mock_get().json = MagicMock(return_value={"symbols":[{"symbol":"AAPL.US","date":"2022-07-29","time":"22:00:11","open":161.24,"high":163.63,"low":159.5,"close":162.51,"volume":101786860,"name":"APPLE"}]})
        response = self.client.get('%s?stock_code=%s' % (reverse('get-stock-service'), 'aapl.us'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'symbol': 'AAPL.US', 'open': 161.24, 'high': 163.63, 'low': 159.5, 'close': 162.51, 'volume': 101786860, 'name': 'APPLE', 'date': '2022-07-29 22:00:11'})