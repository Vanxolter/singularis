from django.core.management.base import BaseCommand

from singularis import settings

import logging
import csv

from transports.models import Airports

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "All airports in the world"

    def handle(self, *args, **options):
        with open(settings.BASE_DIR / "test.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                Airports.objects.create(
                    ident = row[1],
                    type = row[2],
                    name = row[3],
                    latitude_deg = row[4],
                    longitude_deg = row[5],
                    elevation_ft  = row[6],
                    continent = row[7],
                    iso_country = row[8],
                    iso_region = row[9],
                    municipality = row[10],
                    scheduled_service = row[11],
                    gps_code = row[12],
                    iata_code = row[13],
                    local_code = row[14],
                    home_link = row[15],
                    wikipedia_link = row[16],
                    keywords = row[17],
                )
