from rest_framework import generics, permissions
from .models import Staff, Payroll, Attendance, Leave
from .serializers import StaffSerializer, PayrollSerializer, AttendanceSerializer, LeaveSerializer
from django.http import JsonResponse
from .models import Payroll
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Payroll, Staff
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from datetime import datetime
import csv
import datetime
import openpyxl
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Payroll




class StaffListCreateView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]

class PayrollListCreateView(generics.ListCreateAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeaveListCreateView(generics.ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]


def payroll_summary(request, staff_id, year):
    salaries = Payroll.objects.filter(staff__id=staff_id, year=year)
    total_earned = sum(salary.salary_paid + salary.bonus - salary.deductions for salary in salaries)
    total_deductions = sum(salary.deductions for salary in salaries)

    return JsonResponse({
        "total_earned": total_earned,
        "total_deductions": total_deductions
    })

def generate_payslip(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    staff = payroll.staff

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{staff.user.username}_Payslip_{payroll.month}_{payroll.year}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Company: School Name")
    p.drawString(100, 730, f"Payslip for {payroll.month} {payroll.year}")
    p.drawString(100, 710, f"Name: {staff.user.first_name} {staff.user.last_name}")
    p.drawString(100, 690, f"Position: {staff.position}")
    p.drawString(100, 670, f"Bank: {staff.bank_name}")
    p.drawString(100, 650, f"Account Number: {staff.account_number}")
    p.drawString(100, 630, f"Salary Paid: {payroll.salary_paid}")
    p.drawString(100, 610, f"Deductions: {payroll.deductions}")
    p.drawString(100, 590, f"Bonus: {payroll.bonus}")
    p.drawString(100, 570, f"Net Salary: {payroll.net_salary()}")
    p.drawString(100, 550, f"Payment Status: {payroll.payment_status}")

    p.showPage()
    p.save()

    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_payroll(request, payroll_id):
    user = request.user
    if user.role not in ["superadmin", "accountant"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    payroll = get_object_or_404(Payroll, id=payroll_id)
    payroll.approve()

    return Response({"message": "Payroll approved successfully!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payroll_reports(request):
    user = request.user
    if user.role not in ["superadmin", "accountant"]:
        return Response({"error": "Unauthorized"}, status=403)

    total_salary_paid = Payroll.objects.aggregate(total_salary=Sum('salary_paid'))['total_salary']
    total_deductions = Payroll.objects.aggregate(total_deductions=Sum('deductions'))['total_deductions']
    total_bonus = Payroll.objects.aggregate(total_bonus=Sum('bonus'))['total_bonus']
    total_employees = Payroll.objects.values('staff').distinct().count()
    payroll_approved = Payroll.objects.filter(approval_status="Approved").count()
    payroll_pending = Payroll.objects.filter(approval_status="Pending").count()

    return Response({
        "total_salary_paid": total_salary_paid or 0,
        "total_deductions": total_deductions or 0,
        "total_bonus": total_bonus or 0,
        "total_employees": total_employees,
        "payroll_approved": payroll_approved,
        "payroll_pending": payroll_pending
    })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_payroll_csv(request):
    """ Export payroll data as a CSV file """
    if request.user.role not in ["superadmin", "accountant"]:
        return Response({"error": "Unauthorized"}, status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="payroll_{datetime.date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Staff", "Month", "Year", "Salary Paid", "Tax Deduction", "Pension Deduction", "Net Salary", "Status"])

    for payroll in Payroll.objects.all():
        writer.writerow([payroll.staff.user.username, payroll.month, payroll.year, payroll.salary_paid, payroll.tax_deduction, payroll.pension_deduction, payroll.net_salary, payroll.payment_status])

    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_payroll_excel(request):
    """ Export payroll data as an Excel file """
    if request.user.role not in ["superadmin", "accountant"]:
        return Response({"error": "Unauthorized"}, status=403)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="payroll_{datetime.date.today()}.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Payroll Data"

    sheet.append(["Staff", "Month", "Year", "Salary Paid", "Tax Deduction", "Pension Deduction", "Net Salary", "Status"])

    for payroll in Payroll.objects.all():
        sheet.append([payroll.staff.user.username, payroll.month, payroll.year, payroll.salary_paid, payroll.tax_deduction, payroll.pension_deduction, payroll.net_salary, payroll.payment_status])

    workbook.save(response)
    return response

class PayslipHistoryView(ListAPIView):
    """ Retrieve payslip history for an authenticated employee """
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payroll.objects.filter(staff__user=self.request.user).order_by('-year', '-month')