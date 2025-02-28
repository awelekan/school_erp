import csv
import xlwt
from django.http import HttpResponse
from .models import StudentPayment

def export_fees_csv():
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="fee_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Student", "Class Level", "Amount Paid", "Payment Status", "Payment Date"])

    payments = StudentPayment.objects.all()
    for payment in payments:
        writer.writerow([payment.student.username, payment.class_level.name, payment.amount_paid, payment.payment_status, payment.payment_date])

    return response

def export_fees_excel():
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="fee_report.xls"'

    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("Fees")

    columns = ["Student", "Class Level", "Amount Paid", "Payment Status", "Payment Date"]
    for col_num, column_title in enumerate(columns):
        worksheet.write(0, col_num, column_title)

    payments = StudentPayment.objects.all()
    for row_num, payment in enumerate(payments, start=1):
        worksheet.write(row_num, 0, payment.student.username)
        worksheet.write(row_num, 1, payment.class_level.name)
        worksheet.write(row_num, 2, str(payment.amount_paid))
        worksheet.write(row_num, 3, payment.payment_status)
        worksheet.write(row_num, 4, str(payment.payment_date))

    workbook.save(response)
    return response
