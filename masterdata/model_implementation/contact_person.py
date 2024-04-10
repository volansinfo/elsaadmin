import uuid

from django.db import models


class ContactPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    text = models.TextField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contactperson"
        verbose_name_plural = "Contactpersons"
        ordering = ["name"]
