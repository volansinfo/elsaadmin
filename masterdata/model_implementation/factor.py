import uuid

from django.db import models

from masterdata.model_implementation.level import Level
from masterdata.model_implementation.mycotoxin import Mycotoxin
from masterdata.model_implementation.species import Species


class Factor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    species = models.ForeignKey(
        Species, on_delete=models.CASCADE, blank=False, null=False
    )
    mycotoxin = models.ForeignKey(
        Mycotoxin, on_delete=models.CASCADE, blank=False, null=False
    )
    min_level = models.IntegerField()
    max_level = models.IntegerField()
    bw_factor = models.DecimalField(
        decimal_places=2, max_digits=10, blank=False, null=False
    )
    fcr_factor = models.DecimalField(
        decimal_places=2, max_digits=10, blank=False, null=False
    )

    def __str__(self):
        return f"{self.species} for {self.mycotoxin} from {self.min_level} to {self.max_level}"

    class Meta:
        verbose_name = "Factor"
        verbose_name_plural = "Factors"
        ordering = [
            "species",
            "mycotoxin",
            "min_level",
            "max_level",
            "bw_factor",
            "fcr_factor",
        ]
