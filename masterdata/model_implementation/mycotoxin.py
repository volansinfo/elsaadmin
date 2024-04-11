from django.db import models
from django.contrib import admin
from modeltranslation.translator import TranslationOptions, translator


class Mycotoxin(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name="ID")
    text = models.CharField(max_length=255, blank=False, verbose_name="Name")
    val_min = models.IntegerField(verbose_name="Min. value")
    val_max = models.IntegerField(verbose_name="Max. value")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Mycotoxin"
        verbose_name_plural = "Mycotoxins"
        ordering = ("text",)
