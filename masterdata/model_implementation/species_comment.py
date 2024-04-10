from django.db import models
from djrichtextfield.models import RichTextField


class SpeciesComment(models.Model):
    species = models.ForeignKey(
        "masterdata.species", related_name="comments", on_delete=models.CASCADE
    )
    mycotoxin = models.ForeignKey(
        "masterdata.mycotoxin",
        related_name="species_comments",
        on_delete=models.CASCADE,
    )
    level = models.ForeignKey(
        "masterdata.level",
        related_name="species_comments",
        on_delete=models.CASCADE,
    )
    text = RichTextField()

    def __str__(self):
        return f"{self.mycotoxin} at {self.species} on {self.level}"

    class Meta:
        ordering = ["species", "mycotoxin", "level"]
        verbose_name = "Species Comment"
        verbose_name_plural = "Species Comments"
