from django.db import models

from masterdata.model_implementation.sample_type import SampleType


class SpeciesSampleTypeComponents(models.Model):
    species = models.ForeignKey("masterdata.species", on_delete=models.CASCADE)
    sample_type = models.ForeignKey(
        SampleType,
        on_delete=models.CASCADE,
        related_name="sample_type_components",
        null=True,
    )
    raw_components = models.ManyToManyField("masterdata.component", blank=True)

    class Meta:
        ordering = ["species", "sample_type"]
