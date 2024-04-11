from django.db import models

from masterdata.model_implementation.recommendation import (
    RecommendationConfiguration,
    RecommendationException,
)


class ProductRecommendation(models.Model):
    product = models.ForeignKey(
        "masterdata.product",
        on_delete=models.CASCADE,
        related_name="recommendations",
        blank=False,
    )
    text = models.TextField()
    priority = models.IntegerField(
        help_text="The priority decides which product will be picked by default. The highest priority will be picked first."
    )
    recommendation_configuration = models.ForeignKey(
        RecommendationConfiguration, on_delete=models.CASCADE, null=True
    )

    class Meta:
        ordering = ["-priority"]


class ProductRecommendationCountryOverride(models.Model):
    product_recommendation = models.ForeignKey(
        ProductRecommendation,
        on_delete=models.CASCADE,
        related_name="overrides",
    )
    country = models.ForeignKey(
        "masterdata.country",
        on_delete=models.CASCADE,
        related_name="product_recommendation_overrides",
    )
    text = models.TextField()


class ProductExceptionRecommendation(models.Model):
    product = models.ForeignKey(
        "masterdata.product",
        on_delete=models.CASCADE,
        related_name="exception_recommendations",
        blank=False,
    )
    text = models.TextField()
    priority = models.IntegerField(
        help_text="The priority decides which product will be picked by default. The highest priority will be picked first."
    )
    recommendation_configuration = models.ForeignKey(
        RecommendationException, on_delete=models.CASCADE, null=True
    )

    class Meta:
        ordering = ["-priority"]


class ProductExceptionRecommendationCountryOverride(models.Model):
    product_recommendation = models.ForeignKey(
        ProductExceptionRecommendation,
        on_delete=models.CASCADE,
        related_name="exception_overrides",
    )
    country = models.ForeignKey(
        "masterdata.country",
        on_delete=models.CASCADE,
        related_name="product_exception_recommendation_overrides",
    )
    text = models.TextField()
