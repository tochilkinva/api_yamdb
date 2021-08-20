import csv

from django.core.management.base import BaseCommand
from users.models import MyUser


class Command(BaseCommand):
    help = "Команда загружает данные из users.csv в базу данных"

    def handle(self, *args, **options):
        csv_filepath = "static/data/users.csv"

        with open(csv_filepath, newline="") as csvfile:
            data_reader = csv.reader(
                csvfile, delimiter=",", quotechar='"', skipinitialspace=True
            )
            for row in data_reader:
                if row[0] != "id":
                    MyUser.objects.create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                    )
