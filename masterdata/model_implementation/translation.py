from django.db import models


class Translation(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    translation = models.TextField(blank=False)

    class Meta:
        ordering = ["id"]
