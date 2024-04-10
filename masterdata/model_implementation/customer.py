from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["name"]
