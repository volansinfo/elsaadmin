from django.db import models


class Country(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    region = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    display_recommendations = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.text}"

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["id"]
