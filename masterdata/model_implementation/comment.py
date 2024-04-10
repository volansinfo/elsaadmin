from django.db import models
import uuid

from djrichtextfield.models import RichTextField


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    species = models.ForeignKey(
        "masterdata.species", on_delete=models.CASCADE, blank=True
    )
    mycotoxin = models.ForeignKey(
        "masterdata.mycotoxin", on_delete=models.CASCADE, blank=True
    )
    levels = models.ManyToManyField(
        "masterdata.level", blank=True, related_name="comments"
    )
    html = RichTextField()

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = (
            "species",
            "mycotoxin",
        )
