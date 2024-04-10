import uuid

from django.db import models


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    location = models.CharField(max_length=255, blank=False)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]
