import decimal
import random

import string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from masterdata.model_implementation.comment import Comment
from masterdata.model_implementation.component import Component
from masterdata.model_implementation.contact_person import ContactPerson
from masterdata.model_implementation.country import Country
from masterdata.model_implementation.customer import Customer
from masterdata.model_implementation.factor import Factor
from masterdata.model_implementation.interaction import Interaction
from masterdata.model_implementation.laboratory import Laboratory
from masterdata.model_implementation.level import Level
from masterdata.model_implementation.mycotoxin import Mycotoxin
from masterdata.model_implementation.product import Product, ProductCountryRule
from masterdata.model_implementation.recommendation import (
    RecommendationConfiguration,
)
from masterdata.model_implementation.registration_request import (
    RegistrationRequest,
)
from masterdata.model_implementation.sample_type import SampleType
from masterdata.model_implementation.species import Species
from masterdata.model_implementation.species_level import SpeciesLevel
from masterdata.model_implementation.user import User
from masterdata.model_implementation.user_assessment import (
    UserAssessmentRecipient,
    UserAssessmentSample,
    UserAssessmentSampleContamination,
    UserAssessment,
    UserAssessmentProductRecommendation,
    UserAssessmentMovingRisk,
)
from rest_framework import serializers
# from .models import masterdata_axxess

# class AxxessSerializer(serializers.ModelSerializer):
#     #Inclusion_percent = serializers.FloatField(default=30.5)
#     AX_free_ingredients = serializers.IntegerField(default=90)
#     Total_Formulation_Inclusion_percentage = serializers.FloatField(default=100)
#     Total_Formulation_Sol_AX_percentage = serializers.FloatField(default=0.15)
#     Total_Formulation_Insol_AX_percentage = serializers.FloatField(default=0.31)
#     Total_Formulation_ME_KCALperkg = serializers.FloatField(default=336.27)
#     Total_Sol_AX_percent = serializers.FloatField(default=0.15)
#     Total_Insol_AX_percent = serializers.FloatField(default=0.31)
#     Total_Improved_ME_Kcal_per_kg = serializers.FloatField(default=3064)
#     Axxess_XY = serializers.FloatField(default=54.6)

#     Formulation = serializers.FloatField(default=40.2)

#     class Meta:
#         model = masterdata_axxess
#         fields = ['id', 'species', 'ingredients', 'inclusion_percentage','sol_ax', 'insol_ax', 'me', 'ne', 'me_kcal', 'AX_free_ingredients', 'Total_Formulation_Inclusion_percentage', 'Total_Formulation_Sol_AX_percentage', 'Total_Formulation_Insol_AX_percentage', 'Total_Formulation_ME_KCALperkg', 'Total_Sol_AX_percent', 'Total_Insol_AX_percent', 'Total_Improved_ME_Kcal_per_kg', 'Axxess_XY', 'Inclusion_percent', 'Formulation']
# serializers.py

# from rest_framework import serializers
# from .models import masterdata_axxess

# class AxxessSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = masterdata_axxess
#         fields = ['id', 'species', 'ingredients', 'sol_ax', 'insol_ax', 'me_kcal', 'inclusion_percentage']

# class SummarySerializer(serializers.Serializer):
#     Total_Formulation_Inclusion_percentage = serializers.FloatField()
#     Total_Formulation_Sol_AX_percentage = serializers.FloatField()
#     Total_Formulation_Insol_AX_percentage = serializers.FloatField()
#     Total_Formulation_ME_KCALperkg = serializers.FloatField()
#     Total_Sol_AX_percent = serializers.FloatField()
#     Total_Insol_AX_percent = serializers.FloatField()
#     Total_Improved_ME_Kcal_per_kg = serializers.FloatField()
#     Axxess_XY = serializers.FloatField()
#     AX_free_ingredients = serializers.FloatField()


from rest_framework import serializers
from .models import masterdata_axxess

class AxxessSerializer(serializers.ModelSerializer):
    class Meta:
        model = masterdata_axxess
        fields = '__all__'

    def create(self, validated_data):
        return Summary(**validated_data)

    def get_summary(self, result):
        if result:
            inclusion_percentages = [float(data['inclusion_percentage']) for data in result]

            sol_ax_percentages = [float(data['sol_ax']) for data in result]
            total_sol_ax_percentage = round(sum(inclusion * sol_ax / 100 for inclusion, sol_ax in zip(inclusion_percentages, sol_ax_percentages)), 4)

            insol_ax_percentages = [float(data['insol_ax']) for data in result]
            total_insol_ax_percentage = round(sum(inclusion * insol_ax / 100 for inclusion, insol_ax in zip(inclusion_percentages, insol_ax_percentages)), 4)

            me_kcal_percentages = [float(data['me_kcal']) for data in result]
            total_me_kcal_per_kg = round(sum(inclusion * me_kcal / 100 for inclusion, me_kcal in zip(inclusion_percentages, me_kcal_percentages)), 4)

            total_inclusion_percentage = sum(inclusion_percentages)

            ax_free_ingredients = 100 - total_inclusion_percentage  # Calculate AX_free_ingredients

            summary_data = {
                "Total_Formulation_Inclusion_percentage": 100,
                "Total_Formulation_Sol_AX_percentage": total_sol_ax_percentage,
                "Total_Formulation_Insol_AX_percentage": total_insol_ax_percentage,
                "Total_Formulation_ME_KCALperkg": total_me_kcal_per_kg,
                "Total_Sol_AX_percent": total_sol_ax_percentage,
                "Total_Insol_AX_percent": total_insol_ax_percentage,
                "Total_Improved_ME_Kcal_per_kg": 3064,
                "Axxess_XY": 54.6,
                "AX_free_ingredients": ax_free_ingredients
            }
            return summary_data
        else:
            return None








#     class Meta:
#         model = masterdata_axxess
#         fields = ['id', 'species', 'ingredients', 'sol_ax', 'insol_ax', 'me', 'ne', 'me_kcal', 'AX_free_ingredients', 'Total_Formulation_Inclusion_percentage', 'Total_Formulation_Sol_AX_percentage', 'Total_Formulation_Insol_AX_percentage', 'Total_Formulation_ME_KCALperkg', 'Total_Sol_AX_percent', 'Total_Insol_AX_percent', 'Total_Improved_ME_Kcal_per_kg', 'Axxess_XY', 'Inclusion_percent', 'Formulation']
# from rest_framework import serializers
# from .models import masterdata_axxess

# class AxxessSerializer(serializers.ModelSerializer):
#     ingredients = serializers.ListField(child=serializers.CharField())
#     inclusion = serializers.ListField(child=serializers.FloatField())

#     class Meta:
#         model = masterdata_axxess
#         fields = ['species', 'ingredients', 'inclusion']

#     def validate_ingredients(self, value):
#         if not all(isinstance(item, str) for item in value):
#             raise serializers.ValidationError("All ingredients must be strings.")
#         return value


# # serializers.py
# from rest_framework import serializers
# from .models import masterdata_axxess

# class SpeciesIngredientsSerializer(serializers.Serializer):
#     species = serializers.CharField()
#     ingredients = serializers.ListField(child=serializers.CharField())

# from rest_framework import serializers
# from .models import masterdata_axxess

# class AxxessSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = masterdata_axxess
#         fields = ['id', 'species', 'ingredients', 'sol_ax', 'insol_ax', 'me', 'ne', 'me_kcal']

#     def get_ne(self, instance):
#         ne_value = instance.ne
#         if ne_value is None:
#             return 0
#         return ne_value




class SpeciesIngredientsSerializer(serializers.Serializer):
    species = serializers.CharField()
    ingredients = serializers.ListField(child=serializers.CharField())


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "region", "text", "display_recommendations"]


class MycotoxinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mycotoxin
        fields = ["id", "text", "val_min", "val_max"]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            "id",
            "text",
            "color",
            "level_factor",
            "marker_image",
            "result_table_postfix",
            "interpretation_text",
        ]


class SpeciesSerializer(serializers.ModelSerializer):
    has_products = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Species
        fields = ["id", "text", "has_products"]


class ProductCountryRulesSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = ProductCountryRule
        fields = ["country", "name", "logo"]


class ProductsSerializer(serializers.ModelSerializer):
    product_country_rules = ProductCountryRulesSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "product_country_rules", "logo"]


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = ["id", "text"]


class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["id", "text"]


class SampleTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = [
            "id",
            "text",
            "has_inclusion_rate",
            "has_total_risk",
            "has_bw_loss_and_fcr_graph",
        ]


class UserAssessmentRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssessmentRecipient
        fields = ["address"]


class UserAssessmentSampleContaminationSerializer(serializers.ModelSerializer):
    mycotoxin = serializers.PrimaryKeyRelatedField(
        queryset=Mycotoxin.objects.all(), many=False, required=True
    )
    value = serializers.IntegerField(required=True, allow_null=True)
    level = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserAssessmentSampleContamination
        fields = ["mycotoxin", "value", "level"]


class UserAssessmentProductRecommendationSerializer(
    serializers.ModelSerializer
):
    product = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = UserAssessmentProductRecommendation
        fields = ["product", "text"]


class UserAssessmentSampleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)
    component = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Component.objects.all(), many=False
    )
    inclusion_rate = serializers.IntegerField(required=False, allow_null=True)
    contaminations = UserAssessmentSampleContaminationSerializer(many=True)
    risk = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    product_recommendation = UserAssessmentProductRecommendationSerializer(
        many=False, read_only=True
    )
    bw_factor = serializers.DecimalField(
        read_only=True, allow_null=True, decimal_places=2, max_digits=10
    )
    fcr_factor = serializers.DecimalField(
        read_only=True, allow_null=True, decimal_places=2, max_digits=10
    )

    class Meta:
        model = UserAssessmentSample
        fields = [
            "name",
            "component",
            "inclusion_rate",
            "contaminations",
            "risk",
            "product_recommendation",
            "bw_factor",
            "fcr_factor",
        ]


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = ["text"]


class UserSerializer(serializers.ModelSerializer):
    contact_person = ContactPersonSerializer(read_only=True, many=False)

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "ew_status",
            "contact_person",
            "database_access",
            "customer_database_access",
        )


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserAssessmentMovingRiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssessmentMovingRisk
        fields = ["month", "avg_risk_factor", "number_of_assessments"]


class UserAssessmentInputSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    secret_token = serializers.CharField(read_only=True)
    customer_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    customer = serializers.PrimaryKeyRelatedField(
        allow_null=True, read_only=False, queryset=Customer.objects.all()
    )
    author = UserSerializer(allow_null=True, read_only=True, many=False)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), many=False, required=True
    )
    species = serializers.PrimaryKeyRelatedField(
        queryset=Species.objects.all(), many=False, required=True
    )
    test_laboratory = serializers.PrimaryKeyRelatedField(
        queryset=Laboratory.objects.all(), many=False, required=False
    )
    sample_type = serializers.PrimaryKeyRelatedField(
        queryset=SampleType.objects.all(), many=False, required=True
    )
    email_recipients = UserAssessmentRecipientSerializer(many=True)
    selected_product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=False,
        required=False,
        default=None,
        allow_null=True,
    )
    samples = UserAssessmentSampleSerializer(many=True)
    total_risk = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    total_product_recommendation = (
        UserAssessmentProductRecommendationSerializer(
            many=False, read_only=True
        )
    )
    total_bw_factor = serializers.DecimalField(
        read_only=True, allow_null=True, decimal_places=2, max_digits=10
    )
    total_fcr_factor = serializers.DecimalField(
        read_only=True, allow_null=True, decimal_places=2, max_digits=10
    )
    interaction = serializers.CharField(read_only=True)
    comments = serializers.CharField(read_only=True)
    moving_risks = UserAssessmentMovingRiskSerializer(
        many=True, read_only=True
    )

    def _get_level_for_sample(self, species_id, mycotoxin_id, value):
        mycotoxins = {}
        for mycotoxin in Mycotoxin.objects.all():
            mycotoxins[mycotoxin.id] = mycotoxin

        if value < mycotoxins[mycotoxin_id].val_min:
            value = mycotoxins[mycotoxin_id].val_min
        if value > mycotoxins[mycotoxin_id].val_max:
            value = mycotoxins[mycotoxin_id].val_max

        return (
            SpeciesLevel.objects.filter(
                species_id=species_id,
                mycotoxin_id=mycotoxin_id,
                value__gte=value,
            )
            .prefetch_related("level__comments")
            .order_by("value")
            .first()
            .level,
            value,
        )

    def create(self, validated_data):
        email_recipients = validated_data.pop("email_recipients")
        samples = validated_data.pop("samples")
        has_inclusion_rate = validated_data["sample_type"].has_inclusion_rate
        has_total_risk = validated_data["sample_type"].has_total_risk

        added_comment_ids = []
        added_comments = []

        if self.context["request"].user.is_authenticated:
            try:
                interaction = Interaction.objects.get(
                    species_id=validated_data["species"].id
                )
                validated_data["interaction"] = interaction.html
            except Interaction.DoesNotExist:
                pass

        mycotoxins = {}
        for mycotoxin in Mycotoxin.objects.all():
            mycotoxins[mycotoxin.id] = mycotoxin

        secret_token = "".join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits
            )
            for _ in range(100)
        )
        author = None
        if self.context["request"].user.is_authenticated:
            author = self.context["request"].user
        user_assessment: UserAssessment = UserAssessment.objects.create(
            **validated_data, secret_token=secret_token, author=author
        )
        for email_recipient in email_recipients:
            user_assessment.email_recipients.add(
                UserAssessmentRecipient.objects.create(**email_recipient)
            )

        combined_sample = {}

        sample_index = 0
        for sample in samples:
            sample_index = sample_index + 1
            contaminations = sample.pop("contaminations")
            sample_instance: UserAssessmentSample = (
                UserAssessmentSample.objects.create(
                    **sample,
                    sample_index=sample_index,
                    assessment_id=user_assessment.id
                )
            )
            mycotoxin_levels = {}

            if (
                has_inclusion_rate
                and isinstance(sample["inclusion_rate"], int) == False
            ):
                user_assessment.delete()
                raise ValidationError(
                    "You must provide an inclusion_rate if the selected sample type has a inclusion rate!"
                )

            for contamination in contaminations:
                value = contamination["value"]
                if value is not None:
                    if has_inclusion_rate:
                        calculated_value = (
                            sample["inclusion_rate"] / 100
                        ) * value
                        if contamination["mycotoxin"] not in combined_sample:
                            combined_sample[
                                contamination["mycotoxin"]
                            ] = calculated_value
                        else:
                            combined_sample[contamination["mycotoxin"]] = (
                                combined_sample[contamination["mycotoxin"]]
                                + calculated_value
                            )

                    level, cleaned_value = self._get_level_for_sample(
                        species_id=user_assessment.species_id,
                        mycotoxin_id=contamination["mycotoxin"].id,
                        value=value,
                    )
                    if (
                        has_total_risk is False
                        and self.context["request"].user.is_authenticated
                    ):
                        try:
                            factor = Factor.objects.get(
                                species_id=user_assessment.species_id,
                                mycotoxin_id=contamination["mycotoxin"].id,
                                min_level__lte=cleaned_value,
                                max_level__gt=cleaned_value,
                            )
                            prev_bw = (
                                0
                                if sample_instance.bw_factor is None
                                else sample_instance.bw_factor
                            )
                            sample_instance.bw_factor = (
                                prev_bw + factor.bw_factor * value / 1000
                            )
                            prev_fcr = (
                                0
                                if sample_instance.fcr_factor is None
                                else sample_instance.fcr_factor
                            )
                            sample_instance.fcr_factor = (
                                prev_fcr + factor.fcr_factor * value / 1000
                            )
                        except Factor.DoesNotExist:
                            pass
                    if self.context["request"].user.is_authenticated:
                        comments = level.comments.filter(
                            species_id=user_assessment.species_id,
                            mycotoxin_id=contamination["mycotoxin"].id,
                        )
                        for comment in comments:
                            if comment.id not in added_comment_ids:
                                added_comment_ids.append(comment.id)
                                added_comments.append(comment.html)

                    contamination_instance: UserAssessmentSampleContamination = UserAssessmentSampleContamination.objects.create(
                        **contamination, level=level
                    )
                    sample_instance.contaminations.add(contamination_instance)
                    mycotoxin_levels[
                        contamination_instance.mycotoxin_id
                    ] = contamination_instance.level_id
            (
                recommendation,
                product,
            ) = RecommendationConfiguration.objects.get_recommendation(
                species_id=user_assessment.species_id,
                request=self.context["request"],
                selected_product_id=validated_data["selected_product"].id
                if validated_data["selected_product"] is not None
                else None,
                **mycotoxin_levels
            )
            if product is not None:
                product_recommendation = UserAssessmentProductRecommendation(
                    product_id=product.product_id, text=product.text
                )
                product_recommendation.save()
                sample_instance.product_recommendation_id = (
                    product_recommendation.id
                )
            sample_instance.risk_id = recommendation.total_risk_id
            sample_instance.save()
        if (
            self.context["request"].user.is_authenticated
            and self.context["request"].user.customer_database_access
            and user_assessment.customer is not None
        ):

            # generate moving risk
            UserAssessmentMovingRisk.objects.create_moving_risks(
                customer_id=user_assessment.customer_id,
                assessment_id=user_assessment.id,
                species_id=user_assessment.species_id,
            )

            user_assessment.comments = "\n".join(added_comments)
            user_assessment.save()
        if has_inclusion_rate:
            combined_levels = {}
            for mycotoxin_id in combined_sample:

                (lvl, _,) = self._get_level_for_sample(
                    species_id=user_assessment.species_id,
                    mycotoxin_id=mycotoxin_id.id,
                    value=combined_sample[mycotoxin_id],
                )
                combined_levels[mycotoxin_id.id] = lvl.id

            (
                recommendation,
                product,
            ) = RecommendationConfiguration.objects.get_recommendation(
                species_id=user_assessment.species_id,
                request=self.context["request"],
                selected_product_id=validated_data["selected_product"].id
                if validated_data["selected_product"] is not None
                else None,
                **combined_levels
            )
            user_assessment.total_risk_id = recommendation.total_risk_id
            if product is not None:
                product_recommendation = UserAssessmentProductRecommendation(
                    product_id=product.product_id, text=product.text
                )
                product_recommendation.save()
                user_assessment.total_product_recommendation_id = (
                    product_recommendation.id
                )

            # Get factors for combined sample
            if (
                has_total_risk is True
                and self.context["request"].user.is_authenticated
            ):
                for mycotoxin in combined_sample:
                    try:
                        myco = Mycotoxin.objects.get(id=mycotoxin.id)
                        cleaned_value = combined_sample[mycotoxin]
                        if combined_sample[mycotoxin] > myco.val_max:
                            cleaned_value = myco.val_max
                        if combined_sample[mycotoxin] < myco.val_min:
                            cleaned_value = myco.val_min
                        factor = Factor.objects.get(
                            species_id=user_assessment.species_id,
                            mycotoxin_id=mycotoxin,
                            min_level__lte=cleaned_value,
                            max_level__gt=cleaned_value,
                        )
                        prev_bw = (
                            0
                            if user_assessment.total_bw_factor is None
                            else user_assessment.total_bw_factor
                        )
                        user_assessment.total_bw_factor = (
                            prev_bw
                            + factor.bw_factor
                            * decimal.Decimal(combined_sample[mycotoxin])
                            / 1000
                        )
                        prev_fcr = (
                            0
                            if user_assessment.total_fcr_factor is None
                            else user_assessment.total_fcr_factor
                        )
                        user_assessment.total_fcr_factor = (
                            prev_fcr
                            + factor.fcr_factor
                            * decimal.Decimal(combined_sample[mycotoxin])
                            / 1000
                        )
                    except Factor.DoesNotExist:
                        pass

            user_assessment.save()

        return user_assessment

    class Meta:
        model = UserAssessment
        fields = [
            "id",
            "author",
            "created_at",
            "secret_token",
            "customer_name",
            "customer",
            "country",
            "species",
            "test_laboratory",
            "sample_type",
            "email_recipients",
            "samples",
            "selected_product",
            "total_risk",
            "total_product_recommendation",
            "total_bw_factor",
            "total_fcr_factor",
            "interaction",
            "comments",
            "moving_risks",
        ]


# from django.contrib.auth.hashers import make_password
# from rest_framework import serializers
# #from .models import User

# class RegistrationRequestSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "name",
#             "email",
#             "password",
#             "countries",
#             "company",
#             "address of company",
#         ]

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return super().create(validated_data)



# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
# #from .models import User

# class RegistrationRequestSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     country = serializers.CharField(write_only=True)
#     company = serializers.CharField(write_only=True)
#     address_of_company = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "name",
#             "email",
#             "password",
#             "country",
#             "company",
#             "address_of_company",
#         ]

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         country = validated_data.pop('country_id')
#         company = validated_data.pop('company_id')
#         address_of_company = validated_data.pop('address_of_company')
        
#         user = super().create(validated_data)
#         user.country = country
#         user.company = company
#         user.address_of_company = address_of_company
#         user.save()
        
#         return user


# class RegistrationRequestSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     country = serializers.CharField(write_only=True)
#     company = serializers.CharField(write_only=True)
#     address_of_company = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "name",
#             "email",
#             "password",
#             "country",
#             "company",
#             "address_of_company",
#         ]

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         country = validated_data.pop('country')
#         company_name = validated_data.pop('company')
#         address_of_company = validated_data.pop('address_of_company')

#         user = User.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         user.country = country
#         user.company = company_name
#         user.address_of_company = address_of_company

#         user.save()
#         return user


# from rest_framework import serializers


# class RegistrationRequestSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "name",
#             "email",
#             "password",
#         ]

#     def create(self, validated_data):
#         password = validated_data.pop('password')

#         user = User.objects.create(**validated_data)
#         user.set_password(password)

#         user.save()
#         return user

from rest_framework import serializers
#from .models import User

class RegistrationRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField()
    country_name = serializers.CharField()
    company_address = serializers.CharField()
    privacy_policy = serializers.BooleanField(required=False)
    nutrition_verification = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "password",
            "company_name",
            "country_name",
            "company_address",
            "privacy_policy",
            "nutrition_verification",
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        company_name = validated_data.pop('company_name')
        country_name = validated_data.pop('country_name')
        company_address = validated_data.pop('company_address')
        privacy_policy = validated_data.pop('privacy_policy', False)
        nutrition_verification = validated_data.pop('nutrition_verification', False)

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.company_name = company_name
        user.country_name = country_name
        user.company_address = company_address
        user.privacy_policy = privacy_policy
        user.nutrition_verification = nutrition_verification

        user.save()
        return user

















class DatabaseAssessmentSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(read_only=True)
    species = serializers.PrimaryKeyRelatedField(read_only=True)
    test_laboratory = serializers.PrimaryKeyRelatedField(read_only=True)
    sample_type = serializers.PrimaryKeyRelatedField(read_only=True)
    total_risk = serializers.PrimaryKeyRelatedField(read_only=True)
    customer_name = serializers.SerializerMethodField(read_only=True)

    def get_customer_name(self, obj: UserAssessment):
        if obj.customer is None:
            return obj.customer_name
        return obj.customer.name

    class Meta:
        model = UserAssessment
        fields = [
            "id",
            "created_at",
            "country",
            "species",
            "test_laboratory",
            "sample_type",
            "total_risk",
            "total_bw_factor",
            "total_fcr_factor",
            "customer_name",
        ]


class DatabaseSerializer(serializers.ModelSerializer):
    contaminations = UserAssessmentSampleContaminationSerializer(
        many=True, read_only=True
    )
    component = serializers.PrimaryKeyRelatedField(read_only=True)
    risk = serializers.PrimaryKeyRelatedField(read_only=True)
    assessment = DatabaseAssessmentSerializer(read_only=True, many=False)

    class Meta:
        model = UserAssessmentSample
        fields = [
            "id",
            "name",
            "contaminations",
            "component",
            "inclusion_rate",
            "risk",
            "bw_factor",
            "fcr_factor",
            "assessment",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, min_length=1, max_length=255)

    class Meta:
        model = Customer
        fields = ["id", "name"]

# serializers.py

# from rest_framework import serializers
# from .models import CustomUserUser

# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUserUser
#         fields = ('id', 'name', 'email', 'password', 'company', 'country', 'address')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUserUser.objects.create_user(**validated_data)
#         return user

# # class LoginSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField()
# #     password = serializers.CharField()
