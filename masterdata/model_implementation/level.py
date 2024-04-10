from colorfield.fields import ColorField
from django.db import models


class Level(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name="ID")
    text = models.CharField(max_length=255, blank=False, verbose_name="Name")
    color = ColorField(default="#000000")
    level_factor = models.IntegerField(default=0)
    marker_image = models.FileField(blank=True, null=True, default=None)
    result_table_postfix = models.CharField(
        max_length=5, blank=True, verbose_name="Postfix in Results table"
    )
    interpretation_text = models.TextField(
        blank=True, verbose_name="Interpretation text for results"
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"
        ordering = ("text",)
