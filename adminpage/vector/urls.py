from django.urls import path

from vector.views import ExchangeView

urlpatterns = [
    path('exchange/', ExchangeView.as_view(), name='exchange'),
]
