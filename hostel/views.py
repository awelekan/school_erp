from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Hostel, Room, StudentRoomAllocation
from .serializers import *
from .serializers import *
import uuid



class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=True, methods=['post'])
    def allocate_student(self, request, pk=None):
        room = self.get_object()
        student_id = request.data.get("student_id")

        if not student_id:
            return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if room.available_beds < 1:
            return Response({"error": "No available beds in this room"}, status=status.HTTP_400_BAD_REQUEST)

        student_allocation, created = StudentRoomAllocation.objects.get_or_create(
            student_id=student_id,
            defaults={"room": room}
        )

        if not created:
            return Response({"error": "Student already allocated a room"}, status=status.HTTP_400_BAD_REQUEST)

        room.available_beds -= 1
        room.save()
        return Response({"message": "Room allocated successfully"}, status=status.HTTP_201_CREATED)

class StudentRoomAllocationViewSet(viewsets.ModelViewSet):
    queryset = StudentRoomAllocation.objects.all()
    serializer_class = StudentRoomAllocationSerializer




class HostelFeePaymentViewSet(viewsets.ModelViewSet):
    queryset = HostelFeePayment.objects.all()
    serializer_class = HostelFeePaymentSerializer

    @action(detail=True, methods=['post'])
    def initiate_payment(self, request, pk=None):
        """ Initiate payment (integrate with Paystack, Flutterwave, etc.) """
        payment = self.get_object()
        payment.transaction_id = str(uuid.uuid4())  # Generate unique transaction ID
        payment.payment_status = "pending"
        payment.save()
        return Response({"message": "Payment initiated", "transaction_id": payment.transaction_id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def verify_payment(self, request, pk=None):
        """ Verify payment and update status """
        payment = self.get_object()
        # Here, integrate with a payment gateway to verify transaction
        payment.payment_status = "paid"  # Assuming successful payment
        payment.save()
        return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)
