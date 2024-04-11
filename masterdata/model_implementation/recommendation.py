from django.db import models
from rest_framework.request import Request

from masterdata.model_implementation.level import Level
from masterdata.model_implementation.mycotoxin import Mycotoxin


from masterdata.model_implementation.species import Species


class BaseRecommendation(models.Model):
    species_ids = models.ManyToManyField(Species, blank=False)

    total_risk = models.ForeignKey(
        Level, blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class RecommendationConfigurationManager(models.Manager):
    def get_recommendation(
        self, species_id, request: Request, selected_product_id=None, **kwargs
    ):
        from masterdata.model_implementation.mycotoxin_levels import (
            MycotoxinLevels,
        )

        sql_params = []
        sql = f"select distinct on(rec_conf.id) rec_conf.* from {self.model._meta.db_table} rec_conf"
        # masterdata_recommendationconfiguration_species_ids
        sql = (
            sql
            + f" join {self.model.species_ids.through._meta.db_table} mrsi on rec_conf.id = mrsi.recommendationconfiguration_id and mrsi.species_id = %s"
        )
        sql_params.append(species_id)

        mycotoxin_ids = Mycotoxin.objects.values_list("id", flat=True)
        index = 0
        for mycotoxin_id in mycotoxin_ids:
            if mycotoxin_id in kwargs:
                level = kwargs[mycotoxin_id]
            else:
                level = "no"
            sql = (
                sql
                + f" join {MycotoxinLevels._meta.db_table} level_{index} on rec_conf.id = level_{index}.recommendation_configuration_id and level_{index}.mycotoxin_id = %s"
            )
            sql_params.append(mycotoxin_id)

            sql = (
                sql
                + f" join {MycotoxinLevels.levels.through._meta.db_table} levels_{index}_all on level_{index}.id = levels_{index}_all.mycotoxinlevels_id and levels_{index}_all.level_id = %s"
            )
            sql_params.append(level)

            index = index + 1

        exception: RecommendationException = RecommendationException.objects.get_recommendation(
            species_id=species_id,
            request=request,
            selected_product_id=selected_product_id,
            **kwargs,
        )
        if exception is not None:
            print("Exception")
            from masterdata.model_implementation.product_recommendation import (
                ProductExceptionRecommendation,
            )

            product_query = exception.productexceptionrecommendation_set.all()
            if selected_product_id is not None:
                product_query = product_query.filter(
                    product_id=selected_product_id
                )
            if request.user.is_authenticated:
                product_query = product_query.filter(
                    product__in=request.user.products.all()
                )

            if len(product_query) == 1:
                product = product_query.order_by("-priority").first()
            else:
                product = exception.productexceptionrecommendation_set.first()
            return exception, product

        try:
            rc: RecommendationConfiguration = self.raw(sql, sql_params)[0]
            product_query = rc.productrecommendation_set.all()
            if selected_product_id is not None:
                product_query = product_query.filter(
                    product_id=selected_product_id
                )
            if request.user.is_authenticated:
                product_query = product_query.filter(
                    product__in=request.user.products.all()
                )
            from masterdata.model_implementation.product_recommendation import (
                ProductRecommendation,
            )

            if len(product_query) == 1:
                product = product_query.order_by("-priority").first()
            else:
                product = rc.productrecommendation_set.first()
        except RecommendationConfiguration.DoesNotExist:
            rc = None
            product = None

        return rc, product


class RecommendationConfiguration(BaseRecommendation):
    objects = RecommendationConfigurationManager()


class RecommendationExceptionManager(models.Manager):
    def get_recommendation(
        self, species_id, request: Request, selected_product_id=None, **kwargs
    ):
        from masterdata.model_implementation.mycotoxin_levels import (
            MycotoxinExceptionLevels,
        )

        sql_params = []
        sql = f"select distinct on(rec_conf.id) rec_conf.* from {self.model._meta.db_table} rec_conf"
        # masterdata_recommendationconfiguration_species_ids
        sql = (
            sql
            + f" join {self.model.species_ids.through._meta.db_table} mrsi on rec_conf.id = mrsi.recommendationexception_id and mrsi.species_id = %s"
        )
        sql_params.append(species_id)

        mycotoxin_ids = Mycotoxin.objects.values_list("id", flat=True)
        index = 0
        for mycotoxin_id in mycotoxin_ids:
            if mycotoxin_id in kwargs:
                level = kwargs[mycotoxin_id]
            else:
                level = "no"
            sql = (
                sql
                + f" join {MycotoxinExceptionLevels._meta.db_table} level_{index} on rec_conf.id = level_{index}.recommendation_configuration_id and level_{index}.mycotoxin_id = %s"
            )
            sql_params.append(mycotoxin_id)

            sql = (
                sql
                + f" join {MycotoxinExceptionLevels.levels.through._meta.db_table} levels_{index}_all on level_{index}.id = levels_{index}_all.mycotoxinexceptionlevels_id and levels_{index}_all.level_id = %s"
            )
            sql_params.append(level)

            index = index + 1

        try:
            rc = self.raw(sql, sql_params)[0]
        except IndexError:
            rc = None

        return rc


class RecommendationException(BaseRecommendation):
    objects = RecommendationExceptionManager()
