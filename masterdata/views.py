from tempfile import TemporaryFile, NamedTemporaryFile

import django_filters
import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.utils.translation import get_language
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from . import serializers

# Create your views here.
from .model_implementation.component import Component
from .model_implementation.country import Country
from .model_implementation.customer import Customer
from .model_implementation.laboratory import Laboratory
from .model_implementation.level import Level
from .model_implementation.mycotoxin import Mycotoxin
from .model_implementation.product import Product
from .model_implementation.registration_request import RegistrationRequest
from .model_implementation.sample_type import SampleType
from .model_implementation.species import Species
from .model_implementation.species_sample_type_component import (
    SpeciesSampleTypeComponents,
)
from .model_implementation.translation import Translation
from .model_implementation.user import User
from .model_implementation.user_assessment import (
    UserAssessment,
    UserAssessmentSampleFilterSet,
    UserAssessmentSample,
    UserAssessmentMovingRisk,
)
from .permissions import HasCustomerDatabaseAccessOrIsSuperUser
from .serializers import UserSerializer
from .tasks import send_final_report, send_moving_risk_report

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from .models import Axxess  # Import your Axxess model
from .serializers import SpeciesIngredientsSerializer
from .serializers import AxxessSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import masterdata_axxess
from django.http import JsonResponse
from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import masterdata_axxess
# from .serializers import AxxessSerializer

# class AxxessAPIView(APIView):
#     def post(self, request):
#         species = request.data.get('species')
#         ingredients = request.data.getlist('ingredients', [])
#         inclusion_percentages = request.data.getlist('inclusion_percentages', [])

#         queryset = masterdata_axxess.objects.all()

#         if species:
#             queryset = queryset.filter(species=species)

#         if ingredients:
#             queryset = queryset.filter(ingredients__in=ingredients)

#         if inclusion_percentages:
#             for inclusion_percentage in inclusion_percentages:
#                 queryset = queryset.filter(inclusion_percentage=inclusion_percentage)

#         serializer = AxxessSerializer(queryset, many=True)
#         return Response(serializer.data)
# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import masterdata_axxess
from .serializers import AxxessSerializer
from .models import masterdata_axxess
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import masterdata_axxess
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import masterdata_axxess
from .serializers import AxxessSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import masterdata_axxess
# from .serializers import AxxessSerializer, SummarySerializer
# from .models import Formulation
# class AxxessAPIView(APIView):
#     def post(self, request):
#         species = request.data.get('species')
#         ingredients = request.data.get('ingredients')
#         inclusion_percentage = request.data.get('inclusion_percentage')

#         # Split ingredients and inclusion_percentage strings into lists
#         ingredient_list = ingredients.split(',')
#         inclusion_percentage_list = inclusion_percentage.split(',')

#         # Prepare the data for each ingredient
#         result = []
#         for ingredient, percentage in zip(ingredient_list, inclusion_percentage_list):
#             queryset = masterdata_axxess.objects.filter(species=species, ingredients=ingredient)
#             serializer = AxxessSerializer(queryset, many=True)
#             for data in serializer.data:
#                 data['inclusion_percentage'] = percentage
#                 result.append(data)

#         # Add the summary to the result
#         summary_serializer = SummarySerializer()
#         summary_data = summary_serializer.get_summary(result)
#         result.append(summary_data)

#         return Response(result)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import masterdata_axxess, masterdata_formulation
from .serializers import AxxessSerializer

class AxxessAPIView(APIView):
    def post(self, request):
        species = request.data.get('species')
        ingredients = request.data.get('ingredients')
        inclusion_percentage = request.data.get('inclusion_percentage')

        # Split ingredients and inclusion_percentage strings into lists
        ingredient_list = ingredients.split(',')
        inclusion_percentage_list = inclusion_percentage.split(',')

        # Ensure both lists have the same length
        if len(ingredient_list) != len(inclusion_percentage_list):
            return Response({"error": "Number of ingredients and percentages do not match"}, status=400)

        # Prepare the data for each ingredient
        result = []
        total_inclusion_percentage = 0.0
        total_sol_ax_percentage = 0.0
        total_insol_ax_percentage = 0.0
        total_me_kcal_per_kg = 0.0

        for ingredient, percentage in zip(ingredient_list, inclusion_percentage_list):
            queryset = masterdata_axxess.objects.filter(species=species, ingredients=ingredient)
            serializer = AxxessSerializer(queryset, many=True)
            for data in serializer.data:
                data['inclusion_percentage'] = percentage
                result.append(data)
                percentage_float = float(percentage)
                total_inclusion_percentage += percentage_float
                total_sol_ax_percentage += round((float(data['sol_ax']) * percentage_float) / 100, 4)
                total_insol_ax_percentage += round((float(data['insol_ax']) * percentage_float) / 100, 4)
                total_me_kcal_per_kg += round((float(data['me_kcal']) * percentage_float) / 100, 4)

        # Calculate AX free ingredients
        ax_free_ingredients = 100 - total_inclusion_percentage

        # Fetch formulation data
        formulation_data = masterdata_formulation.objects.filter(species=species).values('formulation_Sol_AX', 'formulation_Insol_AX').first()

        if formulation_data:
            # Prepare summary data
            summary_data = {
                "Total_Formulation_Inclusion_percentage": 100,
                "Total_Formulation_Sol_AX_percentage": round(total_sol_ax_percentage, 4),
                "Total_Formulation_Insol_AX_percentage": round(total_insol_ax_percentage, 4),
                "Total_Formulation_ME_KCALperkg": round(total_me_kcal_per_kg, 4),
                "Total_Sol_AX_percent": round(total_sol_ax_percentage, 4),
                "Total_Insol_AX_percent": round(total_insol_ax_percentage, 4),
                "Total_Improved_ME_Kcal_per_kg": round(total_me_kcal_per_kg + (total_sol_ax_percentage * float(formulation_data['formulation_Sol_AX'])) + (total_insol_ax_percentage * float(formulation_data['formulation_Insol_AX'])), 4),
                "Axxess_XY": round(((total_me_kcal_per_kg + (total_sol_ax_percentage * float(formulation_data['formulation_Sol_AX'])) + (total_insol_ax_percentage * float(formulation_data['formulation_Insol_AX']))) - total_me_kcal_per_kg), 4),
                "AX_free_ingredients": ax_free_ingredients,
                "formulation_sol_ax": formulation_data['formulation_Sol_AX'],
                "formulation_insol_ax": formulation_data['formulation_Insol_AX']
            }

            # Add the summary to the result
            result.append(summary_data)
            return Response(result)
        else:
            return Response({"error": "Formulation data not found"}, status=404)

# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import masterdata_axxess, masterdata_formulation
# from .serializers import AxxessSerializer

# class AxxessAPIView(APIView):
#     def post(self, request):
#         species = request.data.get('species')
#         ingredients = request.data.get('ingredients')
#         inclusion_percentage = request.data.get('inclusion_percentage')

#         # Split ingredients and inclusion_percentage strings into lists
#         ingredient_list = ingredients.split(',')
#         inclusion_percentage_list = inclusion_percentage.split(',')

#         # Prepare the data for each ingredient
#         result = []
#         total_inclusion_percentage = 0.0
#         total_sol_ax_percentage = 0.0
#         total_insol_ax_percentage = 0.0
#         total_me_kcal_per_kg = 0.0

#         for ingredient, percentage in zip(ingredient_list, inclusion_percentage_list):
#             queryset = masterdata_axxess.objects.filter(species=species, ingredients=ingredient)
#             serializer = AxxessSerializer(queryset, many=True)
#             for data in serializer.data:
#                 data['inclusion_percentage'] = percentage
#                 result.append(data)
#                 total_inclusion_percentage += float(percentage)
#                 total_sol_ax_percentage += round((float(data['sol_ax']) * float(percentage)) / 100, 4)
#                 total_insol_ax_percentage += round((float(data['insol_ax']) * float(percentage)) / 100, 4)
#                 total_me_kcal_per_kg += round((float(data['me_kcal']) * float(percentage)) / 100, 4)

#         # Calculate AX free ingredients
#         ax_free_ingredients = 100 - total_inclusion_percentage

#         # Fetch formulation data
#         formulation_data = masterdata_formulation.objects.filter(species=species).values('formulation_Sol_AX', 'formulation_Insol_AX').first()


#         # Prepare summary data
#         summary_data = {
#             "Total_Formulation_Inclusion_percentage": 100,
#             "Total_Formulation_Sol_AX_percentage": round(total_sol_ax_percentage, 4),
#             "Total_Formulation_Insol_AX_percentage": round(total_insol_ax_percentage, 4),
#             "Total_Formulation_ME_KCALperkg": round(total_me_kcal_per_kg, 4),
#             "Total_Sol_AX_percent": round(total_sol_ax_percentage, 4),
#             "Total_Insol_AX_percent": round(total_insol_ax_percentage, 4),
#             "Total_Improved_ME_Kcal_per_kg": round(total_me_kcal_per_kg + (total_sol_ax_percentage * float(formulation_data['formulation_Sol_AX'])) + (total_insol_ax_percentage * float(formulation_data['formulation_Insol_AX'])),4),




#             "Axxess_XY": round(((total_me_kcal_per_kg + (total_sol_ax_percentage * float(formulation_data['formulation_Sol_AX'])) + (total_insol_ax_percentage * float(formulation_data['formulation_Insol_AX'])))-total_me_kcal_per_kg),4),
#             "AX_free_ingredients": ax_free_ingredients,
#             "formulation_sol_ax": formulation_data['formulation_Sol_AX'],
#             "formulation_insol_ax": formulation_data['formulation_Insol_AX']
#         }

#         # Add the summary to the result
#         result.append(summary_data)

#         return Response(result)


class CountriesView(generics.ListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.countries
        return Country.objects.all()


class MycotoxinsView(generics.ListAPIView):
    serializer_class = serializers.MycotoxinsSerializer

    def get_queryset(self):
        return Mycotoxin.objects.all()


class SpeciesView(generics.ListAPIView):
    serializer_class = serializers.SpeciesSerializer

    def get_queryset(self):
        return Species.objects.all()


class ProductsView(generics.ListAPIView):
    serializer_class = serializers.ProductsSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.products
        return Product.objects.all()


class LaboratoryView(generics.ListAPIView):
    serializer_class = serializers.LaboratorySerializer

    def get_queryset(self):
        return Laboratory.objects.all()


class SampleTypesView(generics.ListAPIView):
    serializer_class = serializers.SampleTypesSerializer

    def get_queryset(self):
        return SampleType.objects.all()


class LevelsView(generics.ListAPIView):
    serializer_class = serializers.LevelSerializer

    def get_queryset(self):
        return Level.objects.all()


class ComponentsView(generics.ListAPIView):
    serializer_class = serializers.ComponentsSerializer

    def get_queryset(self):
        try:
            instance = SpeciesSampleTypeComponents.objects.get(
                species_id=self.kwargs["species_id"],
                sample_type_id=self.kwargs["sample_type_id"],
            )
            return instance.raw_components.all()
        except SpeciesSampleTypeComponents.DoesNotExist:
            return []


class AllComponentsView(generics.ListAPIView):
    serializer_class = serializers.ComponentsSerializer

    def get_queryset(self):
        return Component.objects.all()


class AssessmentView(generics.CreateAPIView):
    serializer_class = serializers.UserAssessmentInputSerializer

    def get_queryset(self):
        return UserAssessment.objects.all()


class AssessmentDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.UserAssessmentInputSerializer

    def get_object(self):
        return UserAssessment.objects.get(
            id=self.kwargs["id"], secret_token=self.kwargs["secret_token"]
        )


class LanguagesView(APIView):
    def get(self, request, format=None):
        languages = [
            ["en", "English", "English"],
            ["de", "German", "Deutsch"],
            ["es", "Spanish", "español"],
            ["fr", "French", "français"],
            ["pt", "Portuguese", "Português"],
            ["ru", "Russian", "Русский"],
            ["zh-tw", "Traditional Chinese", "简体中文"],
        ]
        return Response(languages)


class TranslationView(APIView):
    def get(self, request, format=None):
        translations = {}
        for translation in Translation.objects.all():
            translations[translation.id] = translation.translation
        return Response(translations)


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


























from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationRequestSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationRequestSerializer

class RegistrationRequestView(APIView):
    def post(self, request):
        serializer = RegistrationRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "registration done"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DatabasePagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class DatabaseView(generics.ListAPIView):
    queryset = UserAssessmentSample.objects.all()
    serializer_class = serializers.DatabaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DatabasePagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_class = UserAssessmentSampleFilterSet
    filterset_fields = [
        "assessment__country",
        "assessment__species",
        "assessment__sample_type",
        "assessment__test_laboratory",
        "assessment__created_at",
        "risk",
        "component",
    ]
    ordering_fields = ["risk", "component", "assessment__created_at"]

    def get_queryset(self):
        if self.request.user.database_access == "none":
            raise PermissionDenied()

        return self.request.user.get_assessment_database().order_by(
            "-assessment__created_at"
        )


class MovingRiskView(generics.GenericAPIView):
    serializer_class = serializers.UserAssessmentMovingRiskSerializer

    @extend_schema(
        responses=serializers.UserAssessmentMovingRiskSerializer(many=True)
    )
    def get(self, request, *args, **kwargs):
        data = UserAssessmentMovingRisk.objects.create_moving_risks(
            customer_id=self.kwargs["customer_id"],
            species_id=self.kwargs["species_id"],
            assessment_id=None,
            for_months=self.kwargs["for_months"],
        )
        data.reverse()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


class SendReportView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None, **kwargs):
        send_final_report.delay(
            lang=get_language(),
            assessment_id=self.kwargs["assessment_id"],
            secret_token=self.kwargs["secret_token"],
        )

        return Response(None, status=status.HTTP_201_CREATED)


class SendMovingRiskReportView(APIView):
    def post(self, request, format=None, **kwargs):
        send_moving_risk_report.delay(
            lang=get_language(),
            receiver_mail_address=self.request.user.email,
            customer_id=self.kwargs["customer_id"],
            species_id=self.kwargs["species_id"],
            for_months=self.kwargs["for_months"],
        )

        return Response(None, status=status.HTTP_201_CREATED)


class CustomerView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        HasCustomerDatabaseAccessOrIsSuperUser,
    ]
    serializer_class = serializers.CustomerSerializer
    filter_backends = [
        SearchFilter,
    ]
    search_fields = ["name"]
    pagination_class = DatabasePagination

    def get_queryset(self):
        return Customer.objects.all()


