from django.db import models
from django.contrib import admin
from modeltranslation.translator import TranslationOptions, translator


class Species(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name="ID")
    text = models.CharField(max_length=255, blank=False, verbose_name="Name")
    has_products = models.ManyToManyField("masterdata.product", blank=True)
    logo = models.ImageField(blank=True, null=True, default=None)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"
        ordering = ("text",)
