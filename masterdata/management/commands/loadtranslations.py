import json
import os

import shutil

import csv
import git
from django.conf import settings
from django.core.management import BaseCommand

from masterdata.model_implementation.translation import Translation


class Command(BaseCommand):
    help = "Imports old translations"

    def flatten_json(self, y):
        out = {}

        def flatten(x, name=""):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + "_")
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + "_")
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    def handle(self, *args, **options):
        self.working_dir = os.path.join(
            settings.BASE_DIR, "masterrisk_translation_import_tmp"
        )
        os.mkdir(self.working_dir)

        try:
            git.Repo.clone_from(
                url=settings.LEGACY_I18N_REPO, to_path=self.working_dir
            )
            Translation.objects.all().delete()
            languages = [lang[0] for lang in settings.LANGUAGES]
            for language in languages:
                self.stdout.write(f"Translating language {language}")
                file_path = os.path.join(
                    self.working_dir, f"src/i18n/{language}.json"
                )
                if os.path.exists(file_path):
                    file_content = open(file_path, "r").read()
                    nested_json = json.loads(file_content)
                    data = self.flatten_json(nested_json)
                    for key in data:
                        orm_key = key.upper()
                        instance, _ = Translation.objects.get_or_create(
                            id=orm_key
                        )
                        setattr(instance, f"translation_{language}", data[key])
                        instance.save()
            with open(
                os.path.join(
                    settings.BASE_DIR, "masterdata/new_translations.csv"
                )
            ) as file:
                reader = csv.reader(file)
                rowCount = 0
                instances = []
                for row in reader:
                    rowCount = rowCount + 1
                    if rowCount != 1:
                        instance = Translation()
                        instance.id = row[0]
                        instance.translation_en = row[1]
                        instance.translation_de = row[2]
                        instance.translation_es = row[3]
                        instance.translation_fr = row[4]
                        instance.translation_pt = row[5]
                        instance.translation_ru = row[6]
                        instance.save()
        finally:
            shutil.rmtree(self.working_dir, ignore_errors=True)
        self.stdout.write(self.style.SUCCESS("Completed translation import"))
