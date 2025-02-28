from rest_framework import serializers
from .models import *
from accounts.models import User

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    
    class Meta:
        model = Student
        fields = '__all__'

class ClassLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
        fields = '__all__'

class ClassArmSerializer(serializers.ModelSerializer):
    level = ClassLevelSerializer()  # Nested for better data representation

    class Meta:
        model = ClassArm
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    class_levels = serializers.PrimaryKeyRelatedField(queryset=ClassLevel.objects.all(), many=True)
    teachers = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'), many=True)

    class Meta:
        model = Subject
        fields = '__all__'
        
class TeacherAssignmentSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    class_arm = serializers.PrimaryKeyRelatedField(queryset=ClassArm.objects.all())

    class Meta:
        model = TeacherAssignment
        fields = '__all__'

class ClassScheduleSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    class_arm = serializers.PrimaryKeyRelatedField(queryset=ClassArm.objects.all())

    class Meta:
        model = ClassSchedule
        fields = '__all__'
        
class MidTermTestSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))

    class Meta:
        model = MidTermTest
        fields = '__all__'

class FinalExamSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))

    class Meta:
        model = FinalExam
        fields = '__all__'

class FinalGradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))
    total_score = serializers.ReadOnlyField()
    grade = serializers.ReadOnlyField()

    class Meta:
        model = FinalGrade
        fields = '__all__'
        
class ReportCardSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    performance_summary = serializers.SerializerMethodField()

    class Meta:
        model = ReportCard
        fields = '__all__'

    def get_performance_summary(self, obj):
        return obj.generate_performance_summary()
    
class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = "__all__"

class AcademicTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTerm
        fields = "__all__"

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"