from django.urls import path
from .views import EmployeeRetrieveAPIView, EmployeeStatsAPIView, ClientsStatsAPIView

urlpatterns = [
    path("statistics/employee/<int:pk>/", EmployeeRetrieveAPIView.as_view(), name="detail-employee"),
    path("employee/statistics/", EmployeeStatsAPIView.as_view(), name="employee-stats"),
    path("statistics/client/<int:pk>/", ClientsStatsAPIView.as_view(), name="client-detail")
]