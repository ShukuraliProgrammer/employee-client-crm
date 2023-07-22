from django.db import models
from django.db.models import Sum


class Employee(models.Model):
    full_name = models.CharField(max_length=120, verbose_name="Full Name")
    birth_date = models.DateField(verbose_name="Birth Date")

    def __str__(self):
        return self.full_name


class Client(models.Model):
    full_name = models.CharField(max_length=120, verbose_name="Full Name")
    birth_date = models.DateField(verbose_name="Birth Date")

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name="Name")
    quantity = models.IntegerField(verbose_name="Quantity")
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="orders")
    price = models.FloatField(verbose_name="Total Price")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Client: {self.client.full_name}| Employee: {self.employee.full_name}"

    def save(self, *args, **kwargs):
        self.price = self.products.aggregate(Sum("price"))["price__sum"]
        super().save(*args, **kwargs)
