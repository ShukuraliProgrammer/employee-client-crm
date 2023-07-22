from django.db.models import Sum
from rest_framework import serializers
from .models import Employee, Client


class EmployeeDetailSerializer(serializers.ModelSerializer):
    clients_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id", "full_name", "clients_count", "products_count", "total_sum",
        )

    def get_clients_count(self, obj):
        return len(set(obj.orders.select_related("client").values_list("client", flat=True)))

    def get_products_count(self, obj):
        return obj.orders.prefetch_related("products").count()

    def get_total_sum(self, obj):
        return obj.orders.aggregate(Sum("price"))["price__sum"]


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id", "full_name"
        )