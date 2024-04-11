import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils import datetime_safe
from datetime import timedelta
from dateutil.relativedelta import *
from django_filters import rest_framework as filters
import typing

from masterdata.model_implementation.country import Country
from masterdata.model_implementation.laboratory import Laboratory
from masterdata.model_implementation.level import Level
from masterdata.model_implementation.mycotoxin import Mycotoxin
from masterdata.model_implementation.product import Product
from masterdata.model_implementation.sample_type import SampleType
from masterdata.model_implementation.species import Species


class UserAssessmentRecipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    address = models.EmailField()


class UserAssessmentSampleContamination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    mycotoxin = models.ForeignKey(
        Mycotoxin, on_delete=models.CASCADE, blank=False
    )
    value = models.IntegerField(blank=True, null=True, default=None)
    level = models.ForeignKey(
        "masterdata.level",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )


class UserAssessmentProductRecommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    text = models.TextField()


class UserAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(
        get_user_model(),
        blank=True,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        related_name="assessments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    secret_token = models.CharField(max_length=100, blank=True)
    customer_name = models.CharField(max_length=255, blank=True, default="")
    customer = models.ForeignKey(
        "masterdata.Customer",
        on_delete=models.SET_NULL,
        related_name="assessments",
        blank=True,
        null=True,
        default=None,
    )
    country = models.ForeignKey(Country, blank=False, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, blank=False, on_delete=models.CASCADE)
    test_laboratory = models.ForeignKey(
        Laboratory,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    sample_type = models.ForeignKey(
        SampleType, blank=False, on_delete=models.CASCADE
    )
    selected_product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    email_recipients = models.ManyToManyField(UserAssessmentRecipient)
    # samples = models.ManyToManyField(UserAssessmentSample, related_name="assessments")
    total_risk = models.ForeignKey(
        Level, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    total_product_recommendation = models.ForeignKey(
        UserAssessmentProductRecommendation,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    total_bw_factor = models.DecimalField(
        null=True, default=None, decimal_places=2, max_digits=10,
    )
    total_fcr_factor = models.DecimalField(
        null=True, default=None, decimal_places=2, max_digits=10,
    )
    interaction = models.TextField(blank=True, default="")
    comments = models.TextField(blank=True, default="")


class UserAssessmentReport(UserAssessment):
    class Meta:
        proxy = True


class UserAssessmentMovingRiskManager(models.Manager):
    def create_moving_risks(
        self,
        customer_id: int,
        species_id: str,
        assessment_id: typing.Optional[uuid.UUID],
        for_months: int = settings.MASTERRISK_MOVING_RISK_FOR_MONTHS,
    ):
        moving_risks = []
        for n in range(for_months):
            month = datetime_safe.datetime.today() - relativedelta(months=n)
            without_total_risk = UserAssessmentSample.objects.filter(
                assessment__created_at__month=month.month,
                assessment__created_at__year=month.year,
                assessment__sample_type__has_total_risk=False,
                assessment__customer_id=customer_id,
                assessment__species_id=species_id,
            ).aggregate(
                avg=models.Avg("risk__level_factor"), count=models.Count("id")
            )
            with_total_risk = UserAssessment.objects.filter(
                created_at__month=month.month,
                created_at__year=month.year,
                sample_type__has_total_risk=True,
                customer_id=customer_id,
                species_id=species_id,
            ).aggregate(
                avg=models.Avg("total_risk__level_factor"),
                count=models.Count("id"),
            )
            if not with_total_risk["avg"]:
                with_total_risk["avg"] = 0
            if not without_total_risk["avg"]:
                without_total_risk["avg"] = 0

            if (
                with_total_risk["count"] != 0
                or without_total_risk["count"] != 0
            ):
                combined_level_factor = (
                    (with_total_risk["avg"] * with_total_risk["count"])
                    + (without_total_risk["avg"] * without_total_risk["count"])
                ) / (with_total_risk["count"] + without_total_risk["count"])
                moving_risks.append(
                    self.create(
                        month=month.date(),
                        avg_risk_factor=combined_level_factor,
                        assessment_id=assessment_id,
                        number_of_assessments=with_total_risk["count"]
                        + without_total_risk["count"],
                    )
                )

        if settings.DEBUG:
            print(f"Calculated {for_months} moving risks:")
            for risk in moving_risks:
                print(f" - Month: {risk.month}, value: {risk.avg_risk_factor}")

        return moving_risks


class UserAssessmentMovingRisk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    month = models.DateField()
    avg_risk_factor = models.DecimalField(max_digits=5, decimal_places=4)
    number_of_assessments = models.IntegerField(default=0)
    assessment = models.ForeignKey(
        UserAssessment,
        on_delete=models.CASCADE,
        related_name="moving_risks",
        blank=True,
        null=True,
        default=None,
    )

    objects = UserAssessmentMovingRiskManager()

    class Meta:
        ordering = ["assessment__id", "month"]


class UserAssessmentSample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=False)
    component = models.ForeignKey(
        "masterdata.component",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    inclusion_rate = models.IntegerField(blank=True, null=True, default=None)
    contaminations = models.ManyToManyField(UserAssessmentSampleContamination)
    risk = models.ForeignKey(
        Level, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    product_recommendation = models.ForeignKey(
        UserAssessmentProductRecommendation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )
    bw_factor = models.DecimalField(
        null=True, default=None, decimal_places=2, max_digits=10,
    )
    fcr_factor = models.DecimalField(
        null=True, default=None, decimal_places=2, max_digits=10,
    )
    sample_index = models.IntegerField(default=0)
    assessment = models.ForeignKey(
        UserAssessment,
        on_delete=models.CASCADE,
        related_name="samples",
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        ordering = ["sample_index"]


class UserAssessmentSampleFilterSet(filters.FilterSet):
    class Meta:
        model = UserAssessmentSample
        fields = {"assessment__created_at": ["lte", "gte", "lt", "gt"]}
