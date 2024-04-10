from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions, translator

from masterdata.model_implementation.comment import Comment
from masterdata.model_implementation.component import Component
from masterdata.model_implementation.country import Country
from masterdata.model_implementation.interaction import Interaction
from masterdata.model_implementation.laboratory import Laboratory
from masterdata.model_implementation.level import Level
from masterdata.model_implementation.mycotoxin import Mycotoxin
from masterdata.model_implementation.product_recommendation import (
    ProductRecommendation,
    ProductExceptionRecommendation,
)
from masterdata.model_implementation.recommendation import (
    RecommendationException,
)
from masterdata.model_implementation.sample_type import SampleType
from masterdata.model_implementation.species import Species
from masterdata.model_implementation.species_comment import SpeciesComment
from masterdata.model_implementation.translation import Translation


@register(Species)
class SpeciesTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Mycotoxin)
class MycotoxinTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Level)
class LevelTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ("html",)


@register(Component)
class ComponentTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ("region", "text")


@register(Interaction)
class InteractionTranslationOptions(TranslationOptions):
    fields = ("html",)


@register(SampleType)
class SampleTypeTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(SpeciesComment)
class SpeciesCommentTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(ProductRecommendation)
class ProductRecommendationTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(ProductExceptionRecommendation)
class ProductRecommendationTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(Translation)
class TranslationTranslationOptions(TranslationOptions):
    fields = ["translation"]


@register(Laboratory)
class LaboratoryTranslationOptions(TranslationOptions):
    fields = ["text"]
