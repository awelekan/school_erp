from django.urls import path
from .views import *

urlpatterns = [
    path('staff/', StaffListCreateView.as_view(), name='staff-list'),
    path('payroll/', PayrollListCreateView.as_view(), name='payroll-list'),
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list'),
    path('leave/', LeaveListCreateView.as_view(), name='leave-list'),
    path('payslip/<int:payroll_id>/', generate_payslip, name='generate-payslip'),
    path('payroll/approve/<int:payroll_id>/', approve_payroll, name='approve-payroll'),
    path('payroll/reports/', payroll_reports, name='payroll-reports'),
    path('payroll/export/csv/', export_payroll_csv, name='export-payroll-csv'),
    path('payroll/export/excel/', export_payroll_excel, name='export-payroll-excel'),
    path('payslip/history/', PayslipHistoryView.as_view(), name='payslip-history'),

]
