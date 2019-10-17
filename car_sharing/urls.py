from django.urls import path

from .views import index, CarView, OrderView, CarList, CarDetail

urlpatterns = [
    path('cars/', CarList.as_view()),
    path('cars/<int:pk>', CarDetail.as_view()),
    path('orders/', OrderView.as_view()),
    path('', index),
]