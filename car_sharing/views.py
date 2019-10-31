from rest_framework.generics import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from .models import Car, Order
from django.contrib.auth.models import User
from .serializers import CarSerializer, OrderSerializer, UserSerializer


def index(request):
    return HttpResponse('Намана')


class OrderView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(instance=orders, many=True)
        return Response({"orders": serializer.data})
    def post(self, request):
        order = request.data.get('order')
        serializer = OrderSerializer(data=order)
        if serializer.is_valid(raise_exception=True):
            order_save = serializer.save()
        return Response({"success": "Order '{}' create successfully".format(order_save.id)})


class CarView(APIView):
    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response({"cars": serializer.data})
    def post(self, request):
        car = request.data
        serializer = CarSerializer(data=car)
        if serializer.is_valid(raise_exception=True):
            car_saved = serializer.save()
        return Response({"success": "Car '{}' create successfully".format(car_saved.model)})

    def put(self, request, pk):
        saved_car = get_object_or_404(Car.objects.all(), pk=pk)
        data = request.data
        serializer = CarSerializer(instance=saved_car, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            car_saved = serializer.save()

        return Response({"success": "Car '{}' update successfully".format(car_saved.model)})

    def delete(self, request, pk):
        car = get_object_or_404(Car.objects.all(), pk=pk)
        car.delete()
        return Response({"message": "Car with id `{}` has been deleted.".format(pk)}, status=204)


class CarList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer