from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('classlevels/', ClassLevelListView.as_view(), name='classlevel-list'),
    path('classarms/', ClassArmListView.as_view(), name='classarm-list'),
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('classlevels/', ClassLevelListView.as_view(), name='classlevel-list'),
    path('classarms/', ClassArmListView.as_view(), name='classarm-list'),
    path('teacher-assignments/', TeacherAssignmentListCreateView.as_view(), name='teacher-assignment-list'),
    path('teacher-assignments/<int:pk>/', TeacherAssignmentDetailView.as_view(), name='teacher-assignment-detail'),
    path('class-schedules/', ClassScheduleListCreateView.as_view(), name='class-schedule-list'),
    path('class-schedules/<int:pk>/', ClassScheduleDetailView.as_view(), name='class-schedule-detail'),
    path('midterm/', MidTermTestListCreateView.as_view(), name='midterm-list'),
    path('midterm/<int:pk>/', MidTermTestDetailView.as_view(), name='midterm-detail'),
    path('exam/', FinalExamListCreateView.as_view(), name='exam-list'),
    path('exam/<int:pk>/', FinalExamDetailView.as_view(), name='exam-detail'),
    path('grades/', FinalGradeListCreateView.as_view(), name='grade-list'),
    path('grades/<int:pk>/', FinalGradeDetailView.as_view(), name='grade-detail'),
    path('report-cards/', ReportCardListCreateView.as_view(), name='report-card-list'),
    path('report-cards/<int:pk>/', ReportCardDetailView.as_view(), name='report-card-detail'),
    path("sessions/", ActiveSessionView.as_view(), name="active_sessions"),
    path("terms/", ActiveTermView.as_view(), name="active_terms"),
    path("enrollment/", StudentEnrollmentView.as_view(), name="student_enrollment"),
    path("promotion/", ClassPromotionView.as_view(), name="class_promotion"),


]
