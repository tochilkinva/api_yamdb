import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Comment, Review

User = get_user_model()


class Command(BaseCommand):
    help = "Команда загружает данные из comments.csv в базу данных"

    def handle(self, *args, **options):
        csv_filepath = "data/comments.csv"

        with open(csv_filepath, newline="", encoding="utf8") as csvfile:
            data_reader = csv.reader(
                csvfile, delimiter=",", quotechar='"', skipinitialspace=True
            )
            for row in data_reader:
                if row[0] != "id":
                    Comment.objects.create(
                        pk=int(row[0]),
                        review=Review.objects.get(pk=int(row[1])),
                        text=row[2],
                        author=User.objects.get(pk=int(row[3])),
                        pub_date=row[4],
                    )
