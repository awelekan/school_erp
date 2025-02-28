from rest_framework import serializers
from .models import *

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class StudentRoomAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRoomAllocation
        fields = '__all__'

class HostelFeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelFeePayment
        fields = '__all__'