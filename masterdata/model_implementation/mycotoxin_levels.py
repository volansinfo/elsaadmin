from django.db import models

from masterdata.model_implementation.recommendation import (
    RecommendationConfiguration,
    RecommendationException,
)


class BaseMycotoxinLevel(models.Model):
    mycotoxin = models.ForeignKey(
        "masterdata.mycotoxin", on_delete=models.CASCADE
    )
    levels = models.ManyToManyField("masterdata.level", blank=True)

    class Meta:
        abstract = True


class MycotoxinLevels(BaseMycotoxinLevel):
    recommendation_configuration = models.ForeignKey(
        RecommendationConfiguration,
        related_name="mycotoxin_regular_levels",
        on_delete=models.CASCADE,
        blank=False,
    )


class MycotoxinExceptionLevels(BaseMycotoxinLevel):
    recommendation_configuration = models.ForeignKey(
        RecommendationException,
        related_name="mycotoxin_exception_levels",
        on_delete=models.CASCADE,
    )
