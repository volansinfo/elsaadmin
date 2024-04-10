import uuid

from django.db import models
from djrichtextfield.models import RichTextField

from masterdata.model_implementation.species import Species


class Interaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    species = models.ForeignKey(
        Species, blank=False, null=False, on_delete=models.CASCADE
    )
    html = RichTextField(blank=False)

    def __str__(self):
        return f"{self.species}"

    class Meta:
        ordering = ["species"]
        verbose_name = "Interaction"
        verbose_name_plural = "Interactions"
