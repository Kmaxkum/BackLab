from rest_framework import serializers

from .models import Car, Order

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'model', 'price', 'status', 'start_use_date', 'end_use_date', 'order']

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.model = validated_data.get('model', instance.model)
        instance.price = validated_data.get('price', instance.price)
        instance.status = validated_data.get('status', instance.status)
        instance.start_use_date = validated_data.get('start_use_date', instance.start_use_date)
        instance.end_use_date = validated_data.get('end_use_date', instance.end_use_date)
        instance.order = validated_data.get('order', instance.order)

        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'comment', 'cars']

    def create(self, validated_data):
        cars_data = validated_data.pop('cars')
        order = Order.objects.create(**validated_data)
        for car_data in cars_data:
            Car.objects.create(order=order, **car_data)
        return order
