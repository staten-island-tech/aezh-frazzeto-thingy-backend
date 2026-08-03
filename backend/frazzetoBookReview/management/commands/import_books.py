import csv
from django.core.management.base import BaseCommand
from frazzetoBookReview.models import Books, Authors


class Command(BaseCommand):
    help = "Import all books from CSV, skipping any book whose title already exists"

    def handle(self, *args, **kwargs):
        added_count = 0
        skipped_count = 0

        with open("Books.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row["title"]

                if Books.objects.filter(title__iexact=title).exists():
                    skipped_count += 1
                    continue

                author, _ = Authors.objects.get_or_create(
                    name=row["author"]
                )
                Books.objects.create(
                    author=author,
                    img=row["thumbnail"],
                    genre=row["genre"][:40],
                    title=title,
                    pageLength=int(row["pages"]) if row["pages"] else 0
                )
                added_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {added_count} added, {skipped_count} skipped (already existed)"
            )
        )
