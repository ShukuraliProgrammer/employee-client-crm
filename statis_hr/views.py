from django.db.models import Q, Sum
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from .serializers import EmployeeDetailSerializer, ClientDetailSerializer
from .models import Employee, Client, Product, Order


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer

    def get(self, request, *args, **kwargs):
        employee = self.get_object()
        month = self.request.query_params.get("month", None)
        year = self.request.query_params.get("year", None)

        if month and year:
            clients_count = len(set(employee.orders.filter(Q(date__month=month), Q(date__year=year)).select_related(
                "client").values_list("client", flat=True)))
            products_count = employee.orders.filter(Q(date__month=month), Q(date__year=year)).prefetch_related(
                "products").count()
            total_sum = employee.orders.filter(Q(date__month=month), Q(date__year=year)).aggregate(Sum("price"))[
                "price__sum"]

        else:
            clients_count = len(set(employee.orders.select_related(
                "client").values_list("client", flat=True)))
            products_count = employee.orders.prefetch_related(
                "products").count()
            total_sum = employee.orders.aggregate(Sum("price"))[
                "price__sum"]

        results = {
            "clients": clients_count,
            "products": products_count,
            "total_sum": total_sum
        }
        return Response(data=results)


class EmployeeStatsAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer

    def get(self, request, *args, **kwargs):
        month = self.request.query_params.get("month", None)
        year = self.request.query_params.get("year", None)

        results = []
        for employee in self.queryset.all():
            if month and year:
                clients_count = len(set(employee.orders.filter(Q(date__month=month), Q(date__year=year)).select_related(
                    "client").values_list("client", flat=True)))
                products_count = employee.orders.filter(Q(date__month=month), Q(date__year=year)).prefetch_related(
                    "products").count()
                total_sum = employee.orders.filter(Q(date__month=month), Q(date__year=year)).aggregate(Sum("price"))[
                    "price__sum"]
            else:
                clients_count = len(set(employee.orders.select_related(
                    "client").values_list("client", flat=True)))
                products_count = employee.orders.prefetch_related(
                    "products").count()
                total_sum = employee.orders.aggregate(Sum("price"))[
                    "price__sum"]

            results.append(
                {"id": employee.id, "clients": clients_count, "products": products_count, "total_sum": total_sum})
        return Response(data=results)


class ClientsStatsAPIView(RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer

    def get(self, request, *args, **kwargs):
        client = self.get_object()

        month = self.request.query_params.get("month", None)
        year = self.request.query_params.get("year", None)

        if month and year:
            products_count = client.orders.filter(Q(date__month=month), Q(date__year=year)).prefetch_related(
                "products").count()
            total_sum = client.orders.filter(Q(date__month=month), Q(date__year=year)).aggregate(Sum("price"))[
                "price__sum"]

        else:
            products_count = client.orders.prefetch_related(
                "products").count()
            total_sum = client.orders.aggregate(Sum("price"))[
                "price__sum"]

        result = {
            "id": client.id,
            "full_name": client.full_name,
            "products": products_count,
            "total_sum": total_sum
        }
        return Response(data=result)
