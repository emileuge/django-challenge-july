# encoding: utf-8

from django.contrib import admin
from django.urls import path

from api import views as api_views

urlpatterns = [
    path('stock', api_views.StockView.as_view(), name='get-stock'),
    path('history', api_views.HistoryView.as_view(), name='get-history'),
    path('stats', api_views.StatsView.as_view(), name='get-stats'),
    path('admin', admin.site.urls),
]
