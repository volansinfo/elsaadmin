from django.core.exceptions import ValidationError
from django.db import models


class SpeciesLevel(models.Model):
    species = models.ForeignKey(
        "masterdata.species", related_name="levels", on_delete=models.CASCADE
    )
    mycotoxin = models.ForeignKey(
        "masterdata.mycotoxin",
        related_name="species_levels",
        on_delete=models.CASCADE,
    )
    level = models.ForeignKey(
        "masterdata.level",
        related_name="species_levels",
        on_delete=models.CASCADE,
    )
    value = models.IntegerField()

    def clean(self):
        super().clean()
        if self.value < self.mycotoxin.val_min:
            raise ValidationError(
                f"Value must be at least the configured min value of {self.mycotoxin.val_min}."
            )
        if self.value > self.mycotoxin.val_max:
            raise ValidationError(
                f"Value must be smaller or equals than the configured max value of {self.mycotoxin.val_max}."
            )

    def __str__(self):
        return f"{self.level} on {self.species} with {self.mycotoxin}"

    class Meta:
        ordering = ["species", "mycotoxin", "value"]
        verbose_name = "Species Level Definition"
        verbose_name_plural = "Species Level Definitions"
        unique_together = ["species", "mycotoxin", "level"]
