from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bus, Driver, Route, Stop, StudentTransport, TransportFee
from .serializers import *
from .services import PaymentGateway


# Bus Management
class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticated]

# Driver Management
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

# Route Management
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

# Stop Management
class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    permission_classes = [permissions.IsAuthenticated]

# Student Transport Assignment
class StudentTransportViewSet(viewsets.ModelViewSet):
    queryset = StudentTransport.objects.all()
    serializer_class = StudentTransportSerializer
    permission_classes = [permissions.IsAuthenticated]

# Transport Fee Management
class TransportFeeViewSet(viewsets.ModelViewSet):
    queryset = TransportFee.objects.all()
    serializer_class = TransportFeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def initiate_payment(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            payment_method = serializer.validated_data["payment_method"]
            email = request.user.email

            payment_response = PaymentGateway.initialize_payment(amount, email, payment_method)
            if payment_response and payment_response.get("status"):
                return Response({"payment_url": payment_response["data"]["authorization_url"]}, status=status.HTTP_200_OK)
            return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def verify_payment(self, request, pk=None):
        transport_fee = self.get_object()
        if transport_fee.status == "paid":
            return Response({"message": "Already paid"}, status=status.HTTP_200_OK)

        payment_response = PaymentGateway.verify_payment(transport_fee.payment_method, transport_fee.transaction_ref)
        if payment_response and payment_response.get("status"):
            transport_fee.status = "paid"
            transport_fee.paid_at = now()
            transport_fee.save()
            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)

        return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        # Your logic for verifying payment
        return Response({"message": "Payment verified"}, status=status.HTTP_200_OK)
