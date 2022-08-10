# encoding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import requests
from datetime import datetime

class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('stock_code')
        r = requests.get(f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=json')
        r.raise_for_status
        r = r.json()
        if not r or not r['symbols'][0]:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                r = r['symbols'][0]
                received_date = r.pop('date')
                received_time = r.pop('time')
                received_at = datetime.strptime(received_date + ' ' + received_time, '%Y-%m-%d %H:%M:%S')
                r['date'] = received_at.strftime("%Y-%m-%d %H:%M:%S")
                return JsonResponse(r)
            except Exception as e:
                msg = "Error: {}".format(e)
                return Response(status=status.HTTP_400_BAD_REQUEST,
                            exception=True, data={'message': msg})

