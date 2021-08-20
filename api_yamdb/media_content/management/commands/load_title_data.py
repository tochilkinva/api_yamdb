import csv
from django.core.management.base import BaseCommand
from media_content.models import Title, Category


class Command(BaseCommand):
    help = "Команда загружает данные из title.csv в базу данных"

    def handle(self, *args, **options):
        csv_filepath = "data/titles.csv"

        with open(csv_filepath, newline="") as csvfile:
            data_reader = csv.reader(
                csvfile, delimiter=",", quotechar='"', skipinitialspace=True
            )
            for row in data_reader:
                if row[0] != "id":
                    Title.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=Category.objects.get(pk=row[3]),
                    )
