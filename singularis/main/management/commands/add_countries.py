from django.core.management.base import BaseCommand

from main.models import Countries
from singularis import settings

import logging
import csv


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "All Countries in the world"

    def handle(self, *args, **options):
        with open(settings.BASE_DIR / "countries.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                Countries.objects.create(
                    code = row[1],
                    name = row[2],
                    continent = row[3],
                    wikipedia_link = row[4],
                    keywords = row[5],
                )
