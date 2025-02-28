from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import StudentPayment
from .payment_gateway import initialize_paystack_payment, verify_paystack_payment
from django.http import FileResponse
from .utils import generate_payment_receipt
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import send_fee_reminders
from django.http import FileResponse
from .export_utils import export_fees_csv, export_fees_excel



class FeeCategoryListCreateView(generics.ListCreateAPIView):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class FeeStructureListCreateView(generics.ListCreateAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiscountListCreateView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]



def student_fee_statement(request, student_id, session, term):
    summary = PaymentSummary(student_id, session, term)
    return JsonResponse({
        "total_fees_due": summary.total_fees_due(),
        "total_discounts": summary.total_discounts(),
        "total_paid": summary.total_paid(),
        "balance_due": summary.balance_due()
    })


class FeeStructureViewSet(viewsets.ModelViewSet):
    """ Manage Fee Structure (Only Superadmin/Accountant) """
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAuthenticated]

class StudentPaymentViewSet(viewsets.ModelViewSet):
    """ View Student Payments """
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'student':
            return StudentPayment.objects.filter(student=self.request.user)
        return super().get_queryset()

class DiscountViewSet(viewsets.ModelViewSet):
    """ Manage Discounts """
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

class ScholarshipViewSet(viewsets.ModelViewSet):
    """ Manage Scholarships """
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAuthenticated]


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        payment_method = request.data.get("payment_method", "paystack")

        if payment_method == "paystack":
            response = initialize_paystack_payment(amount, request.user.email)
            return Response(response)

        return Response({"error": "Unsupported payment method"}, status=400)

class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reference = request.data.get("reference")
        payment_method = request.data.get("payment_method", "paystack")

        if payment_method == "paystack":
            response = verify_paystack_payment(reference)
            if response.get("status") == "success":
                # Update payment record
                StudentPayment.objects.filter(transaction_reference=reference).update(
                    payment_status="completed"
                )
                return Response({"message": "Payment verified successfully"})

        return Response({"error": "Payment verification failed"}, status=400)

class PaymentReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        return generate_payment_receipt(payment_id)
    
    
class SendFeeReminderView(APIView):
    def get(self, request):
        send_fee_reminders.delay()
        return Response({"message": "Fee reminders are being processed!"})
    
class FeeReportsView(APIView):
    def get(self, request):
        total_collected = StudentPayment.objects.filter(payment_status="completed").aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
        total_pending = StudentPayment.objects.filter(payment_status="pending").aggregate(Sum("class_level__fee_amount"))["class_level__fee_amount__sum"] or 0
        class_wise_fees = StudentPayment.objects.values("class_level__name").annotate(total_paid=Sum("amount_paid"))

        return Response({
            "total_collected": total_collected,
            "total_pending": total_pending,
            "class_wise_fees": class_wise_fees
        })
        


class ExportFeesCSVView(APIView):
    def get(self, request):
        return export_fees_csv()

class ExportFeesExcelView(APIView):
    def get(self, request):
        return export_fees_excel()
