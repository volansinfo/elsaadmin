import uuid

from django.db import models


class Component(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ["text"]
