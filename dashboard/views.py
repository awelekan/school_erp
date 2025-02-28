from django.db.models import Count, Sum, Avg
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from academics.models import Student, ClassLevel, Subject, FinalGrade
from finance.models import Payment
from transport.models import *
from hostel.models import *
from hr.models import Payroll
from .permissions import IsSuperadminOrControllerOrAccountant
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class DashboardAPIView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if not request.user.is_superuser and not request.user.role in ['Controller', 'Accountant']:
            return Response({'error': 'Access Denied'}, status=403)

        # Student Statistics
        total_students = Student.objects.count()
        students_per_class = Student.objects.values('current_class__name').annotate(count=Count('id'))

        # Teacher Statistics
        total_teachers = ClassLevel.objects.values('class_teacher').distinct().count()
        teachers_per_subject = Subject.objects.values('teacher__username').annotate(count=Count('id'))

        # Fee Collection Statistics
        total_revenue = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        outstanding_fees = Payment.objects.filter(is_paid=False).aggregate(Sum('amount_due'))['amount_due__sum'] or 0

        # Student Performance
        avg_performance = FinalGrade.objects.aggregate(Avg('total_marks'))['total_marks__avg'] or 0

        # Payroll Summary
        total_salaries_paid = Payroll.objects.aggregate(Sum('net_salary'))['net_salary__sum'] or 0

        # Transport & Hostel Stats
        transport_users = StudentTransport.objects.count()
        hostel_occupancy = StudentRoomAllocation.objects.count()

        data = {
            'students': {
                'total': total_students,
                'per_class': list(students_per_class)
            },
            'teachers': {
                'total': total_teachers,
                'per_subject': list(teachers_per_subject)
            },
            'finance': {
                'total_revenue': total_revenue,
                'outstanding_fees': outstanding_fees,
            },
            'performance': {
                'average_score': avg_performance,
            },
            'payroll': {
                'total_salaries_paid': total_salaries_paid,
            },
            'transport': {
                'total_users': transport_users,
            },
            'hostel': {
                'occupancy': hostel_occupancy,
            }
        }
        return Response(data)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsSuperadminOrControllerOrAccountant]

    def get(self, request):
        total_students = Student.objects.count()
        active_students = Student.objects.filter(is_active=True).count()
        graduated_students = Student.objects.filter(status="Graduated").count()

        total_teachers = Student.objects.values('teacher').distinct().count()

        # Fee and Payroll Insights (only visible to Superadmin, Controller, Accountant)
        total_fees_collected = Payment.objects.filter(status="Paid").aggregate(Sum('amount'))['amount__sum'] or 0
        outstanding_fees = Payment.objects.filter(status="Pending").aggregate(Sum('amount'))['amount__sum'] or 0
        total_salary_paid = Payroll.objects.filter(status="Paid").aggregate(Sum('amount'))['amount__sum'] or 0

        avg_scores = FinalGrade.objects.aggregate(Avg('total_score'))['total_score__avg'] or 0
        top_students = Student.objects.annotate(avg_score=Avg('exam__total_score')).order_by('-avg_score')[:5]

        total_transport_users = TransportFee.objects.count()
        total_hostel_students = HostelFeePayment.objects.count()

        return Response({
            "students": {"total": total_students, "active": active_students, "graduated": graduated_students},
            "teachers": {"total": total_teachers},
            "fees": {
                "total_collected": total_fees_collected,
                "outstanding": outstanding_fees
            },
            "performance": {
                "average_score": avg_scores,
                "top_students": [{"name": s.user.get_full_name(), "score": s.avg_score} for s in top_students],
            },
            "payroll": {"total_paid": total_salary_paid},
            "transport": {"total_users": total_transport_users},
            "hostel": {"total_students": total_hostel_students},
        })