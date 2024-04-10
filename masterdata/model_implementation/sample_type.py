from django.db import models


class SampleType(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    text = models.CharField(max_length=255)
    has_inclusion_rate = models.BooleanField(default=False)
    has_total_risk = models.BooleanField(default=False)
    has_bw_loss_and_fcr_graph = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["text"]
        verbose_name = "Sample Type"
        verbose_name_plural = "Sample Types"
