import csv

from django.core.management.base import BaseCommand
from frazzetoBookReview.models import Books, Authors


class Command(BaseCommand):
    help = "Import all books from CSV"

    def handle(self, *args, **kwargs):
        with open("data.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                author, _ = Authors.objects.get_or_create(
                    name=row["authors"]
                )

                Books.objects.create(
                    author=author,
                    img=row["thumbnail"],
                    genre=row["categories"][:40],
                    title=row["title"][:100],
                    pageLength=int(row["num_pages"]) if row["num_pages"] else 0
                )

        self.stdout.write(
            self.style.SUCCESS("All books imported successfully")
        )
