from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import StudentPayment

def generate_payment_receipt(payment_id):
    payment = StudentPayment.objects.get(id=payment_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.student.username}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 800, "School Payment Receipt")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Student: {payment.student.username}")
    p.drawString(100, 750, f"Class Level: {payment.class_level}")
    p.drawString(100, 730, f"Amount Paid: ₦{payment.amount_paid}")
    p.drawString(100, 710, f"Payment Status: {payment.payment_status}")
    p.drawString(100, 690, f"Transaction Reference: {payment.transaction_reference}")
    
    p.showPage()
    p.save()
    
    return response
