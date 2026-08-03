import csv
from django.core.management.base import BaseCommand
from frazzetoBookReview.models import Books, Authors


class Command(BaseCommand):
    help = "Import all books from CSV, skipping any book whose title already exists"

    def handle(self, *args, **kwargs):
        added_count = 0
        skipped_count = 0

        with open("data.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row["title"][:100]

                if Books.objects.filter(title__iexact=title).exists():
                    skipped_count += 1
                    continue

                author, _ = Authors.objects.get_or_create(
                    name=row["authors"]
                )

                pages_raw = row["pages"]
                pageLength = int(pages_raw) if pages_raw and pages_raw.isdigit() else 0

                Books.objects.create(
                    author=author,
                    img=row["thumbnail"],
                    genre=row["categories"][:40],
                    title=title,
                    pageLength=pageLength
                )
                added_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {added_count} added, {skipped_count} skipped (already existed)"
            )
        )
