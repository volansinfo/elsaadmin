from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.utils import model_ngettext
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext, gettext_lazy
from rangefilter.filter import DateRangeFilter
from modeltranslation.admin import (
    TranslationBaseModelAdmin,
    TranslationAdmin,
    TabbedTranslationAdmin,
    TranslationTabularInline,
    TabbedDjangoJqueryTranslationAdmin,
    TranslationStackedInline,
)
from modeltranslation.translator import TranslationOptions, translator

from masterdata.forms import UserAdminChangeForm, UserAdminCreationForm
from masterdata.model_implementation.comment import Comment
from masterdata.model_implementation.company import Company
from masterdata.model_implementation.component import Component
from masterdata.model_implementation.contact_person import ContactPerson
from masterdata.model_implementation.country import Country
from masterdata.model_implementation.customer import Customer
from masterdata.model_implementation.factor import Factor
from masterdata.model_implementation.interaction import Interaction
from masterdata.model_implementation.laboratory import Laboratory
from masterdata.model_implementation.level import Level
from masterdata.model_implementation.mycotoxin import Mycotoxin
from masterdata.model_implementation.mycotoxin_levels import (
    MycotoxinLevels,
    MycotoxinExceptionLevels,
)
from masterdata.model_implementation.product import ProductCountryRule, Product
from masterdata.model_implementation.product_recommendation import (
    ProductRecommendation,
    ProductExceptionRecommendation,
)
from masterdata.model_implementation.recommendation import (
    BaseRecommendation,
    RecommendationConfiguration,
    RecommendationException,
)
from masterdata.model_implementation.sample_type import SampleType
from masterdata.model_implementation.species import Species
from masterdata.model_implementation.species_comment import SpeciesComment
from masterdata.model_implementation.species_level import SpeciesLevel
from masterdata.model_implementation.species_sample_type_component import (
    SpeciesSampleTypeComponents,
)
from masterdata.model_implementation.translation import Translation
from masterdata.model_implementation.user import User
from masterdata.model_implementation.user_assessment import (
    UserAssessmentReport,
)


class SpeciesAdmin(TabbedTranslationAdmin):
    list_display = ("id", "text")
    search_fields = ("id", "text")


admin.site.register(Species, SpeciesAdmin)


class MycotoxinAdmin(TabbedTranslationAdmin):
    list_display = ("id", "text", "val_min", "val_max")
    search_fields = ("id", "text")


admin.site.register(Mycotoxin, MycotoxinAdmin)


class LevelAdmin(TabbedTranslationAdmin):
    list_display = (
        "id",
        "text",
    )
    search_fields = ("id", "text")


admin.site.register(Level, LevelAdmin)


class CommentAdmin(TabbedTranslationAdmin):
    autocomplete_fields = ("species", "mycotoxin", "levels")
    list_display = (
        "species",
        "mycotoxin",
    )
    list_filter = ("species", "mycotoxin")


admin.site.register(Comment, CommentAdmin)


class EWTranslationAdmin(TabbedTranslationAdmin):
    search_fields = ("id", "translation")
    list_display = ("id", "translation")


admin.site.register(Translation, EWTranslationAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "location"]
    search_fields = ["name", "location"]
    fields = ["name", "location", "info"]


admin.site.register(Company, CompanyAdmin)


class ComponentAdmin(TabbedTranslationAdmin):
    list_display = ["text"]
    search_fields = ["text"]


admin.site.register(Component, ComponentAdmin)


class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(ContactPerson, ContactPersonAdmin)


class CountryAdmin(TabbedTranslationAdmin):
    list_display = ["id", "region", "text"]
    search_fields = ["text"]


admin.site.register(Country, CountryAdmin)


class FactorAdmin(admin.ModelAdmin):
    list_display = [
        "species",
        "mycotoxin",
        "min_level",
        "max_level",
        "bw_factor",
        "fcr_factor",
    ]
    list_filter = ["species", "mycotoxin"]
    list_editable = ["min_level", "max_level", "bw_factor", "fcr_factor"]
    autocomplete_fields = [
        "species",
        "mycotoxin",
    ]


admin.site.register(Factor, FactorAdmin)


class InteractionAdmin(TabbedTranslationAdmin):
    list_display = ["species"]
    autocomplete_fields = ["species"]


admin.site.register(Interaction, InteractionAdmin)


class SampleTypeAdmin(TabbedTranslationAdmin):
    list_display = ["text"]
    search_fields = ["text"]


admin.site.register(SampleType, SampleTypeAdmin)


class SpeciesCommentAdmin(TabbedTranslationAdmin):
    list_display = ["species", "mycotoxin", "level"]
    autocomplete_fields = ["species", "mycotoxin", "level"]


admin.site.register(SpeciesComment, SpeciesCommentAdmin)


class LaboratoryAdmin(TabbedTranslationAdmin):
    list_display = ["id", "text"]


admin.site.register(Laboratory, LaboratoryAdmin)


class SpeciesLevelAdmin(admin.ModelAdmin):
    list_display = [
        "species",
        "mycotoxin",
        "level",
        "value",
    ]
    list_filter = ["species", "mycotoxin", "level"]
    autocomplete_fields = ["species", "mycotoxin", "level"]


admin.site.register(SpeciesLevel, SpeciesLevelAdmin)


class SpeciesSampleTypeComponentsAdmin(admin.ModelAdmin):
    list_display = ["species", "sample_type"]
    list_filter = ["species", "sample_type"]
    autocomplete_fields = ["species", "sample_type", "raw_components"]


admin.site.register(
    SpeciesSampleTypeComponents, SpeciesSampleTypeComponentsAdmin
)


class ProductCountryRuleInlineAdmin(admin.TabularInline):
    model = ProductCountryRule
    fields = ["country", "name", "logo"]
    autocomplete_fields = ["country"]
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    inlines = [ProductCountryRuleInlineAdmin]


admin.site.register(Product, ProductAdmin)


class MycotoxinLevelsInlineAdmin(admin.TabularInline):
    model = MycotoxinLevels
    fields = ["mycotoxin", "levels"]
    autocomplete_fields = ["mycotoxin", "levels"]
    extra = 0


class MycotoxinExceptionsLevelsInlineAdmin(admin.TabularInline):
    model = MycotoxinExceptionLevels
    fields = ["mycotoxin", "levels"]
    autocomplete_fields = ["mycotoxin", "levels"]
    extra = 0


class ProductRecommendationInlineAdmin(TranslationStackedInline):
    model = ProductRecommendation
    fields = ["product", "text", "priority"]
    autocomplete_fields = ["product"]
    extra = 0


class ProductRecommendationExceptionsInlineAdmin(TranslationStackedInline):
    model = ProductExceptionRecommendation
    fields = ["product", "text", "priority"]
    autocomplete_fields = ["product"]
    extra = 0


class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["species_list", "mycotoxin_levels", "total_risk"]
    list_filter = ["species_ids", "total_risk"]
    autocomplete_fields = ["species_ids", "total_risk"]
    inlines = [MycotoxinLevelsInlineAdmin, ProductRecommendationInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related(
            "species_ids",
            "mycotoxin_regular_levels",
            "mycotoxin_regular_levels__levels",
        )
        return qs

    def species_list(self, obj: RecommendationConfiguration):
        return mark_safe(
            "<br>".join(
                [f"- {species.text}" for species in obj.species_ids.all()]
            )
        )

    def mycotoxin_levels(self, obj: RecommendationConfiguration):
        return mark_safe(
            "<br>".join(
                [
                    f"- {mycotoxin_level.mycotoxin} ({', '.join(level.text for level in mycotoxin_level.levels.all())})"
                    for mycotoxin_level in obj.mycotoxin_regular_levels.all()
                ]
            )
        )

    class Media:
        js = (
            "modeltranslation/js/force_jquery.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


admin.site.register(RecommendationConfiguration, RecommendationAdmin)


class RecommendationExceptionAdmin(admin.ModelAdmin):
    list_display = ["species_list", "mycotoxin_levels", "total_risk"]
    list_filter = ["species_ids", "total_risk"]
    autocomplete_fields = ["species_ids", "total_risk"]
    inlines = [
        MycotoxinExceptionsLevelsInlineAdmin,
        ProductRecommendationExceptionsInlineAdmin,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related(
            "species_ids",
            "mycotoxin_exception_levels",
            "mycotoxin_exception_levels__levels",
        )
        return qs

    def species_list(self, obj: RecommendationException):
        return mark_safe(
            "<br>".join(
                [f"- {species.text}" for species in obj.species_ids.all()]
            )
        )

    def mycotoxin_levels(self, obj: RecommendationException):
        return mark_safe(
            "<br>".join(
                [
                    f"- {mycotoxin_level.mycotoxin} ({', '.join(level.text for level in mycotoxin_level.levels.all())})"
                    for mycotoxin_level in obj.mycotoxin_exception_levels.all()
                ]
            )
        )

    class Media:
        js = (
            "modeltranslation/js/force_jquery.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


admin.site.register(RecommendationException, RecommendationExceptionAdmin)


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "email",
        "name",
        "is_superuser",
        "is_staff",
        "ew_status",
        "database_access",
    )
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            "Personal info",
            {"fields": (("email", "name"), ("company", "contact_person"))},
        ),
        (
            "MasterRisk Settings",
            {
                "fields": (
                    "countries",
                    "products",
                    "ew_status",
                    "notify_on_registrations",
                    ("database_access", "customer_database_access"),
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    ("is_active", "is_staff", "is_superuser"),
                    ("groups",),
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "name")
    ordering = ("name",)
    filter_horizontal = ()
    autocomplete_fields = (
        "groups",
        "countries",
        "products",
        "company",
        "contact_person",
    )


admin.site.register(User, CustomUserAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


admin.site.register(Customer, CustomerAdmin)
