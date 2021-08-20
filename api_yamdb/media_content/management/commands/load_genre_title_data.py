import csv
from django.core.management.base import BaseCommand
from media_content.models import Title, Genre


class Command(BaseCommand):
    help = "Команда загружает данные из genre_title.csv в базу данных"

    def handle(self, *args, **options):
        csv_filepath = "data/genre_title.csv"

        with open(csv_filepath, newline="") as csvfile:
            data_reader = csv.reader(
                csvfile, delimiter=",", quotechar='"', skipinitialspace=True
            )
            for row in data_reader:
                if row[0] != "id":
                    title = Title.objects.get(id=row[1])
                    genre = Genre.objects.get(id=row[2])
                    title.genre.add(genre)
