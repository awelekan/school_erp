from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .promotion import promote_students
from rest_framework.parsers import MultiPartParser
from .utils import process_csv


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [AllowAny]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassLevelListView(generics.ListAPIView):
    queryset = ClassLevel.objects.all()
    serializer_class = ClassLevelSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassArmListView(generics.ListAPIView):
    queryset = ClassArm.objects.all()
    serializer_class = ClassArmSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherAssignmentListCreateView(generics.ListCreateAPIView):
    queryset = TeacherAssignment.objects.all()
    serializer_class = TeacherAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeacherAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherAssignment.objects.all()
    serializer_class = TeacherAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassScheduleListCreateView(generics.ListCreateAPIView):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

class MidTermTestListCreateView(generics.ListCreateAPIView):
    queryset = MidTermTest.objects.all()
    serializer_class = MidTermTestSerializer
    permission_classes = [permissions.IsAuthenticated]

class MidTermTestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MidTermTest.objects.all()
    serializer_class = MidTermTestSerializer
    permission_classes = [permissions.IsAuthenticated]

class FinalExamListCreateView(generics.ListCreateAPIView):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class FinalExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinalExam.objects.all()
    serializer_class = FinalExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class FinalGradeListCreateView(generics.ListCreateAPIView):
    queryset = FinalGrade.objects.all()
    serializer_class = FinalGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

class FinalGradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinalGrade.objects.all()
    serializer_class = FinalGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReportCardListCreateView(generics.ListCreateAPIView):
    queryset = ReportCard.objects.all()
    serializer_class = ReportCardSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReportCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportCard.objects.all()
    serializer_class = ReportCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
@api_view(["GET"])
def generate_report_pdf(request, student_id, term, session):
    try:
        report_card = ReportCard.objects.get(student_id=student_id, term=term, session=session)
        grades = FinalGrade.objects.filter(student_id=student_id)

        template_path = 'report_card_template.html'
        context = {'report_card': report_card, 'grades': grades}

        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="report_card_{student_id}.pdf"'
        pisa.CreatePDF(html, dest=response)

        return response
    except ReportCard.DoesNotExist:
        return HttpResponse("Report card not found", status=404)

class ActiveSessionView(generics.ListAPIView):
    queryset = AcademicSession.objects.filter(is_active=True)
    serializer_class = AcademicSessionSerializer

class ActiveTermView(generics.ListAPIView):
    queryset = AcademicTerm.objects.filter(is_active=True)
    serializer_class = AcademicTermSerializer

class StudentEnrollmentView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
class ClassPromotionView(APIView):
    def get(self, request):
        message = promote_students()
        return Response({"message": message})
    
    
class BulkEnrollmentView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES["file"]
        message = process_csv(file)
        return Response({"message": message})