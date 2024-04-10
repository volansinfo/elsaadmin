from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views
from django.contrib import admin
from django.urls import include, path
from django.urls import path
from .views import AxxessAPIView
# urls.py
from .views import RegistrationRequestView
from django.urls import path
from . import views

from django.urls import path
from .views import RegistrationRequestView

urlpatterns = [
    path('registration-request/', RegistrationRequestView.as_view(), name='registration_request'),
    # Other URL patterns for your project
]



urlpatterns = [
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path('axxess/', AxxessAPIView.as_view(), name='masterdata-axxess'),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path(
        "languages/",
        views.LanguagesView.as_view(),
        name="masterdata-languages",
    ),
    path(
        "countries/",
        views.CountriesView.as_view(),
        name="masterdata-countries",
    ),
    path(
        "mycotoxins/",
        views.MycotoxinsView.as_view(),
        name="masterdata-mycotoxins",
    ),
    path("species/", views.SpeciesView.as_view(), name="masterdata-species"),
    path(
        "products/", views.ProductsView.as_view(), name="masterdata-products"
    ),
    path(
        "laboratories/",
        views.LaboratoryView.as_view(),
        name="masterdata-laboratories",
    ),
    path(
        "sample-types/",
        views.SampleTypesView.as_view(),
        name="masterdata-sample-types",
    ),
    path(
        "components/",
        views.AllComponentsView.as_view(),
        name="masterdata-all-components",
    ),
    path(
        "components/<str:species_id>/<str:sample_type_id>/",
        views.ComponentsView.as_view(),
        name="masterdata-components",
    ),
    path(
        "assessment/",
        views.AssessmentView.as_view(),
        name="masterdata-assessment",
    ),

    path(
        "assessment/<str:id>/<str:secret_token>/",
        views.AssessmentDetailView.as_view(),
        name="masterdata-assessment-detail",
    ),
    path(
        "register/",
        RegistrationRequestView.as_view(),
        name="masterdata-register",
    ),
    path("levels/", views.LevelsView.as_view(), name="masterdata-levels"),
    path("user/", views.UserDetailView.as_view(), name="masterdata-user"),
    path(
        "user/change-password/",
        views.ChangePasswordView.as_view(),
        name="masterdata-user-change-password",
    ),
    path(
        "translations/",
        views.TranslationView.as_view(),
        name="masterdata-translations",
    ),
    path(
        "database/", views.DatabaseView.as_view(), name="masterdata-database"
    ),
    path(
        "customers/", views.CustomerView.as_view(), name="masterdata-customers"
    ),
    path(
        "customers/<int:customer_id>/moving-risk/<str:species_id>/<int:for_months>/",
        views.MovingRiskView.as_view(),
        name="masterdata-moving-risk",
    ),
    path(
        "customers/<int:customer_id>/moving-risk/<str:species_id>/<int:for_months>/send-report/",
        views.SendMovingRiskReportView.as_view(),
        name="masterdata-send-moving-risk",
    ),
    path(
        "send-report/<str:assessment_id>/<str:secret_token>/",
        views.SendReportView.as_view(),
        name="masterdata-send-report",
    ),
]
