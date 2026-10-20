import json
from pathlib import Path

from dateutil.parser import parse as parse_datetime
from django.core.management.base import BaseCommand

from ...models import Article, Medium


class Command(BaseCommand):
    help = "Load articles from a JSON archive written by export_articles."

    def add_arguments(self, parser):
        parser.add_argument("path", type=Path)

    def handle(self, *args, **options):
        data = json.loads(options["path"].read_text(encoding="utf-8"))
        media = {medium.slug: medium for medium in Medium.objects.all()}
        imported = 0
        for item in data:
            medium = media.get(item["medium"])
            if not medium:
                continue
            Article.objects.update_or_create(
                medium=medium,
                guid=item["guid"],
                defaults={
                    "title": item["title"],
                    "description": item["description"],
                    "url": item["url"],
                    "image_url": item["image_url"],
                    "published_at": parse_datetime(item["published_at"]),
                },
            )
            imported += 1
        self.stdout.write(f"Imported {imported} articles from {options['path']}")
