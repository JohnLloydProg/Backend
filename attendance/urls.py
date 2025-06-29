from django.urls import path
from attendance import views


urlpatterns = [
    path('qr-code', views.QRCodeView.as_view(), name='qr code'),
    path('logging', views.LoggingView.as_view(), name='logging'),
    path('attendances/<int:year>/<int:month>/<int:day>', views.AttendanceView.as_view(), name='attendances'),
]
