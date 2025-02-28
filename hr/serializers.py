from rest_framework import serializers
from .models import Staff, Payroll, Attendance, Leave

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class PayrollSerializer(serializers.ModelSerializer):
    net_salary = serializers.SerializerMethodField()

    class Meta:
        model = Payroll
        fields = '__all__'

    def get_net_salary(self, obj):
        return obj.net_salary()

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
