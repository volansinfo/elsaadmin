import json
import os

import shutil

import csv
from collections import defaultdict

import git
import markdown
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from masterdata.model_implementation.comment import Comment
from masterdata.model_implementation.company import Company
from masterdata.model_implementation.component import Component
from masterdata.model_implementation.contact_person import ContactPerson
from masterdata.model_implementation.country import Country
from masterdata.model_implementation.factor import Factor
from masterdata.model_implementation.interaction import Interaction
from masterdata.model_implementation.laboratory import Laboratory
from masterdata.model_implementation.level import Level
from masterdata.model_implementation.mycotoxin import Mycotoxin
from masterdata.model_implementation.mycotoxin_levels import (
    MycotoxinLevels,
    MycotoxinExceptionLevels,
)
from masterdata.model_implementation.product import Product, ProductCountryRule
from masterdata.model_implementation.product_recommendation import (
    ProductRecommendation,
    ProductRecommendationCountryOverride,
    ProductExceptionRecommendation,
    ProductExceptionRecommendationCountryOverride,
)
from masterdata.model_implementation.recommendation import (
    RecommendationConfiguration,
    RecommendationException,
)
from masterdata.model_implementation.sample_type import SampleType
from masterdata.model_implementation.species import Species
from masterdata.model_implementation.species_level import SpeciesLevel
from masterdata.model_implementation.species_sample_type_component import (
    SpeciesSampleTypeComponents,
)
from masterdata.model_implementation.user import User


class Command(BaseCommand):
    help = "Imports masterdata in legacy format"

    def handle(self, *args, **options):
        self.working_dir = os.path.join(
            settings.BASE_DIR, "masterrisk_data_import_tmp"
        )
        os.mkdir(self.working_dir)
        try:
            git.Repo.clone_from(
                url=settings.LEGACY_DATA_REPO, to_path=self.working_dir
            )
            self._load_contact_persons()
            self._load_companies()
            self._load_components()
            self._load_countries()
            self._load_levels()
            self._load_products()
            self._load_mycotoxins()
            self._load_laboratories()
            self._load_sample_types()
            self._load_species()
            self._load_species_levels()
            self._load_recommendation_exceptions()
            self._load_species_sample_type_components()
            self._load_comments()
            self._load_factors()
            self._load_recommendations()
            self._load_users()

        finally:
            shutil.rmtree(self.working_dir, ignore_errors=True)
        self.stdout.write(self.style.SUCCESS("This command actually works!"))

    def _load_users(self):
        with open(os.path.join(self.working_dir, "CSV/accounts.csv")) as file:
            reader = csv.reader(file)
            rowCount = 0
            created_users = 0
            updated_users = 0

            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    try:
                        user = User.objects.get(email__iexact=row[0])
                        User.objects.update_user_from_csv(
                            user=user,
                            name=row[1],
                            country_access=row[3].split(";"),
                            product_acces=row[4].split(";"),
                            status=row[5],
                            company_id=row[6],
                            contact_person_id=row[7],
                            backend_user=row[8],
                        )
                    except User.DoesNotExist:
                        User.objects.import_user_from_csv(
                            email=row[0],
                            name=row[1],
                            country_access=row[3].split(";"),
                            product_acces=row[4].split(";"),
                            status=row[5],
                            company_id=row[6],
                            contact_person_id=row[7],
                            backend_user=row[8],
                        )

            print(
                f"Created {created_users} users, Updated {updated_users} users"
            )

    def _load_contact_persons(self):
        ContactPerson.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/contactPersonId.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = ContactPerson()
                    instance.name = row[0]
                    instance.text = row[1]
                    instances.append(instance)
            ContactPerson.objects.bulk_create(instances, 100)

    def _load_companies(self):
        Company.objects.all().delete()
        with open(os.path.join(self.working_dir, "CSV/companyId.csv")) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = Company()
                    instance.name = row[0]
                    instance.location = row[1]
                    instance.info = row[2]
                    instances.append(instance)
            Company.objects.bulk_create(instances, 100)

    def _load_levels(self):
        Level.objects.all().delete()
        with open(os.path.join(self.working_dir, "CSV/levelsId.csv")) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = Level()
                    instance.id = row[0]
                    instance.text_en = row[1]
                    instance.text_de = row[2]
                    instance.text_es = row[3]
                    instance.text_fr = row[4]
                    instance.text_pt = row[5]
                    instance.text_ru = row[6]
                    if row[0] == "no":
                        instance.level_factor = 0
                    if row[0] == "low":
                        instance.color = "#76923c"
                        instance.level_factor = 1
                    elif row[0] == "medium":
                        instance.color = "#f9bf01"
                        instance.level_factor = 2
                    elif row[0] == "high":
                        instance.color = "#a40b00"
                        instance.level_factor = 3
                    elif row[0] == "severe":
                        instance.color = "#f81700"
                        instance.level_factor = 4
                    instances.append(instance)
            Level.objects.bulk_create(instances, 100)

    def _load_countries(self):
        Country.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/countriesId.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = Country()
                    instance.id = row[0]
                    instance.region = row[1]
                    instance.text_en = row[2]
                    instance.text_de = row[3]
                    instance.text_es = row[4]
                    instance.text_fr = row[5]
                    instance.text_pt = row[6]
                    instance.text_ru = row[7]
                    if instance.id == "US":
                        instance.display_recommendations = False
                    instances.append(instance)
            Country.objects.bulk_create(instances, 100)

    def _load_products(self):
        ProductCountryRule.objects.all().delete()
        Product.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/productsId.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    product = Product()
                    product.id = row[0]
                    product.name = row[1]
                    product.save()
                    rule = ProductCountryRule()
                    rule.country_id = "US"
                    rule.name = row[2]
                    rule.product_id = product.id
                    rule.save()

    def _load_mycotoxins(self):
        Mycotoxin.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/mycotoxinsId.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = Mycotoxin()
                    instance.id = row[0]
                    instance.val_min = int(row[1])
                    instance.val_max = int(row[2])
                    instance.text_en = row[3]
                    instance.text_de = row[4]
                    instance.text_es = row[5]
                    instance.text_fr = row[6]
                    instance.text_pt = row[7]
                    instance.text_ru = row[8]
                    instance.save()

    def _load_components(self):
        Component.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/componentsId.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = Component()
                    instance.id = row[0]
                    instance.text_en = row[1]
                    instance.text_de = row[2]
                    instance.text_es = row[3]
                    instance.text_fr = row[4]
                    instance.text_pt = row[5]
                    instance.text_ru = row[6]
                    instance.save()

    def _load_laboratories(self):
        Laboratory.objects.all().delete()
        Laboratory(id="internal", text="Internal").save()
        Laboratory(id="external", text="External").save()

    def _load_sample_types(self):
        SampleType.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/sampleTypesId.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = SampleType()
                    instance.id = row[0]
                    instance.text_en = row[1]
                    instance.text_de = row[2]
                    instance.text_es = row[3]
                    instance.text_fr = row[4]
                    instance.text_pt = row[5]
                    instance.text_ru = row[6]
                    if row[0] == "diet":
                        instance.has_inclusion_rate = True
                        instance.has_total_risk = True
                    instance.save()

    def _load_comments(self):
        Comment.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/comment/commentsId.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            last_species_id = ""
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    if row[1] != "":
                        if row[0] == "":
                            row[0] = last_species_id
                        last_species_id = row[0]
                        instance = Comment()
                        instance.species_id = row[0]
                        instance.mycotoxin_id = row[1]

                        langs = [
                            (3, "en"),
                            (4, "de"),
                            (5, "es"),
                            (6, "fr"),
                            (7, "pt"),
                            (8, "ru"),
                        ]
                        for lang in langs:
                            filename = row[lang[0]]
                            path = os.path.join(
                                self.working_dir, f"CSV/comment/{filename}.md",
                            )
                            if os.path.exists(path):
                                markdown_content = open(path, "r").read()
                                setattr(
                                    instance,
                                    f"html_{lang[1]}",
                                    markdown.markdown(markdown_content),
                                )
                        instance.save()
                        for level in row[2].split(";"):
                            instance.levels.add(level)

    def _load_species(self):
        Species.objects.all().delete()
        Interaction.objects.all().delete()
        with open(os.path.join(self.working_dir, "CSV/speciesId.csv")) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    instance = Species()
                    instance.id = row[0]
                    instance.text_en = row[1]
                    instance.text_de = row[2]
                    instance.text_es = row[3]
                    instance.text_fr = row[4]
                    instance.text_pt = row[5]
                    instance.text_ru = row[6]
                    instance.save()
                    for productId in row[7].split(";"):
                        instance.has_products.add(productId)
                    interaction_instance = Interaction()
                    interaction_instance.species_id = instance.id
                    languages = [lang[0] for lang in settings.LANGUAGES]
                    for language in languages:
                        path = os.path.join(
                            self.working_dir,
                            f"CSV/comment/{instance.id}InteractionsComments{language.capitalize()}.md",
                        )
                        if os.path.exists(path):
                            markdown_content = open(path, "r").read()
                            setattr(
                                interaction_instance,
                                f"html_{language}",
                                markdown.markdown(markdown_content),
                            )
                    interaction_instance.save()

    def _load_species_levels(self):
        SpeciesLevel.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/speciesLevels.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    if row[2] == "noRisk":
                        row[2] = "no"
                    instance = SpeciesLevel()
                    instance.species_id = row[0]
                    instance.mycotoxin_id = row[1]
                    instance.level_id = row[2]
                    instance.value = (
                        int(row[4]) - 1
                        if row[3] == "0"
                        else Mycotoxin.objects.get(id=row[1]).val_max
                    )
                    # instance.value_type = "maximum" if row[3] == "0" else "minimum"
                    instance.save()

    def _load_factors(self):
        Factor.objects.all().delete()
        with open(os.path.join(self.working_dir, "CSV/factors.csv")) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    for species_id in row[0].split(";"):
                        instance = Factor()
                        instance.species_id = species_id
                        instance.mycotoxin_id = row[1]
                        instance.min_level = int(row[2])
                        instance.max_level = int(row[3])
                        instance.bw_factor = float(row[4].replace(",", "."))
                        instance.fcr_factor = float(row[5].replace(",", "."))
                        instance.save()

    def _load_species_sample_type_components(self):
        SpeciesSampleTypeComponents.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/speciesComponents.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            instances = []
            last_species_ids = ""
            last_component_ids = ""
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    if row[0] == "":
                        row[0] = last_species_ids
                    last_species_ids = row[0]
                    if row[1] == "":
                        row[1] = last_component_ids
                    last_component_ids = row[1]
                    for species_id in row[0].split(";"):
                        for sample_type_id in row[1].split(";"):
                            (
                                instance,
                                _,
                            ) = SpeciesSampleTypeComponents.objects.get_or_create(
                                species_id=species_id,
                                sample_type_id=sample_type_id,
                            )
                            try:
                                instance.raw_components.add(row[2])
                            except IntegrityError:
                                self.stdout.write(
                                    f"Could not add raw component {row[2]}!"
                                )

    def _load_recommendation_exceptions(self):
        RecommendationException.objects.all().delete()
        with open(
            os.path.join(self.working_dir, "CSV/recommendationsExceptions.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            last_species_id = ""
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    if row[0] == "":
                        row[0] = last_species_id
                    last_species_id = row[0]
                    rc: RecommendationException = RecommendationException.objects.create(
                        total_risk_id=None if row[13] == "" else row[13]
                    )
                    for species in row[0].split(";"):
                        rc.species_ids.add(species)
                    for mycotoxin in [
                        ["afla", 2],
                        ["don", 4],
                        ["fum", 6],
                        ["ota", 8],
                        ["tTox", 10],
                        ["zea", 12],
                    ]:
                        myco_level: MycotoxinExceptionLevels = MycotoxinExceptionLevels.objects.create(
                            recommendation_configuration_id=rc.id,
                            mycotoxin_id=mycotoxin[0],
                        )
                        if row[mycotoxin[1]] != "":
                            for level in row[mycotoxin[1]].split(";"):
                                if level != "":
                                    myco_level.levels.add(level)
                    for recommendation in [[14, 30], [17, 20], [20, 10]]:
                        if row[recommendation[0]] not in ["", "none"]:
                            # Fix Typos in CSV file
                            if row[recommendation[0]].upper() == "MS":
                                row[recommendation[0]] = "Ms"
                            elif row[recommendation[0]].upper() == "MSFM":
                                row[recommendation[0]] = "MsFm"
                            elif row[recommendation[0]].upper() == "MSGLD":
                                row[recommendation[0]] = "MsGld"
                            elif row[recommendation[0]].upper() == "MSP":
                                row[recommendation[0]] = "MsP"
                            product_recommendation: ProductExceptionRecommendation = ProductExceptionRecommendation.objects.create(
                                product_id=row[recommendation[0]],
                                text=row[recommendation[0] + 1],
                                priority=recommendation[1],
                                recommendation_configuration_id=rc.id,
                            )
                            ProductExceptionRecommendationCountryOverride.objects.create(
                                product_recommendation_id=product_recommendation.id,
                                country_id="US",
                                text=row[recommendation[0] + 2],
                            )

    def _load_recommendations(self):
        RecommendationConfiguration.objects.all().delete()
        # exceptions = self._load_recommendation_exceptions()
        with open(
            os.path.join(self.working_dir, "CSV/recommendations.csv")
        ) as file:
            reader = csv.reader(file)
            rowCount = 0
            last_species_id = ""
            for row in reader:
                rowCount = rowCount + 1
                if rowCount != 1:
                    if row[0] == "":
                        row[0] = last_species_id
                    last_species_id = row[0]
                    rc: RecommendationConfiguration = RecommendationConfiguration.objects.create(
                        total_risk_id=None if row[13] == "" else row[13]
                    )
                    for species in row[0].split(";"):
                        rc.species_ids.add(species)
                    for mycotoxin in [
                        ["afla", 2],
                        ["don", 4],
                        ["fum", 6],
                        ["ota", 8],
                        ["tTox", 10],
                        ["zea", 12],
                    ]:
                        myco_level: MycotoxinLevels = MycotoxinLevels.objects.create(
                            recommendation_configuration_id=rc.id,
                            mycotoxin_id=mycotoxin[0],
                        )
                        if row[mycotoxin[1]] != "":
                            for level in row[mycotoxin[1]].split(";"):
                                if level != "":
                                    myco_level.levels.add(level)
                    for recommendation in [[14, 30], [17, 20], [20, 10]]:
                        if row[recommendation[0]] not in ["", "none"]:
                            # Fix Typos in CSV file
                            if row[recommendation[0]].upper() == "MS":
                                row[recommendation[0]] = "Ms"
                            elif row[recommendation[0]].upper() == "MSFM":
                                row[recommendation[0]] = "MsFm"
                            elif row[recommendation[0]].upper() == "MSGLD":
                                row[recommendation[0]] = "MsGld"
                            elif row[recommendation[0]].upper() == "MSP":
                                row[recommendation[0]] = "MsP"
                            product_recommendation: ProductRecommendation = ProductRecommendation.objects.create(
                                product_id=row[recommendation[0]],
                                text=row[recommendation[0] + 1],
                                priority=recommendation[1],
                                recommendation_configuration_id=rc.id,
                            )
                            ProductRecommendationCountryOverride.objects.create(
                                product_recommendation_id=product_recommendation.id,
                                country_id="US",
                                text=row[recommendation[0] + 2],
                            )
