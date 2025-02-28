from rest_framework import serializers
from .models import *

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    stops = serializers.PrimaryKeyRelatedField(many=True, queryset=Stop.objects.all())

    class Meta:
        model = Route
        fields = '__all__'

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'

class StudentTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTransport
        fields = '__all__'

class TransportFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportFee
        fields = '__all__'

class PaymentInitiateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=['paystack', 'flutterwave', 'bank_transfer', 'cash'])