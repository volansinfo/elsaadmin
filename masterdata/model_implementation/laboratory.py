from django.db import models


class Laboratory(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    text = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]
        verbose_name = "Laboratory"
        verbose_name_plural = "Laboratories"
