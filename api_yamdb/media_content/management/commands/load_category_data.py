import csv
from django.core.management.base import BaseCommand
from media_content.models import Category


class Command(BaseCommand):
    help = "Команда загружает данные из category.csv в базу данных"

    def handle(self, *args, **options):
        csv_filepath = "data/category.csv"

        with open(csv_filepath, newline="") as csvfile:
            data_reader = csv.reader(
                csvfile, delimiter=",", quotechar='"', skipinitialspace=True
            )
            for row in data_reader:
                if row[0] != "id":
                    Category.objects.create(
                        id=row[0], name=row[1], slug=row[2]
                    )
