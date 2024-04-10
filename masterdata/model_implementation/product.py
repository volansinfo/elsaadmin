import uuid

from django.db import models

from masterdata.model_implementation.country import Country


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    logo = models.ImageField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Products"
        verbose_name_plural = "Products"


class ProductCountryRule(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="product_country_rules",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="product_country_rules",
    )
    logo = models.ImageField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Deviating Product Name"
        verbose_name_plural = "Deviating Product Names"
