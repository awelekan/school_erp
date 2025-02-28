from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('fees', FeeStructureViewSet)
router.register('payments', StudentPaymentViewSet)
router.register('discounts', DiscountViewSet)
router.register('scholarships', ScholarshipViewSet)


urlpatterns = [
    path('fee-categories/', FeeCategoryListCreateView.as_view(), name='fee-category-list'),
    path('fee-structures/', FeeStructureListCreateView.as_view(), name='fee-structure-list'),
    path('discounts/', DiscountListCreateView.as_view(), name='discount-list'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
    path("payment/initiate/", InitiatePaymentView.as_view(), name="initiate_payment"),
    path("payment/verify/", VerifyPaymentView.as_view(), name="verify_payment"),
    path("payment/receipt/<int:payment_id>/", PaymentReceiptView.as_view(), name="payment_receipt"),
    path("payment/reminders/", SendFeeReminderView.as_view(), name="send_fee_reminders"),
    path("payment/reports/", FeeReportsView.as_view(), name="fee_reports"),
    path("payment/export/csv/", ExportFeesCSVView.as_view(), name="export_fees_csv"),
    path("payment/export/excel/", ExportFeesExcelView.as_view(), name="export_fees_excel"),

    
    path('', include(router.urls))

]
