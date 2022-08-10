# encoding: utf-8

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
import requests
from django.http import JsonResponse
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Count, F

@permission_classes([IsAuthenticated])
class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')
        r = requests.get('http://localhost:8080/stock?stock_code='+stock_code)
        r.raise_for_status
        if r.status_code == 200:
            r = r.json()
            if r:
                UserRequestHistory.objects.create(
                    date=datetime.strptime(r['date'], '%Y-%m-%d %H:%M:%S'),
                    name=r['name'],
                    symbol=r['symbol'],
                    open=r['open'],
                    high=r['high'],
                    low=r['low'],
                    close=r['close'],
                    user=request.user
                )
                return JsonResponse(r)
            
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class HistoryView(generics.ListAPIView):
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer
    pagination_class = None
    """
    Returns queries made by current user.
    """
    def get(self, request, *args, **kwargs):
        data = UserRequestHistory.objects.filter(user=request.user)\
            .values('date', 'name', 'symbol', 'open', 'high', 'low', 'close')
        return Response(data, status=status.HTTP_200_OK)

@permission_classes([IsAdminUser])
class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.
    def get(self, request, *args, **kwargs):
        data = UserRequestHistory.objects.values('symbol')\
            .annotate(times_requested=Count('symbol'))\
                .annotate(stock=F('symbol'))\
                .order_by('-times_requested')[:5]
        return Response(data, status=status.HTTP_200_OK)
