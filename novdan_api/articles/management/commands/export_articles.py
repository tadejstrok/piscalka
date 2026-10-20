import json
from pathlib import Path

from django.core.management.base import BaseCommand

from ...models import Article


class Command(BaseCommand):
    help = "Write all articles to a JSON archive (stable output, oldest last)."

    def add_arguments(self, parser):
        parser.add_argument("path", type=Path)
        parser.add_argument("--medium", help="Only export this medium slug.")

    def handle(self, *args, **options):
        articles = Article.objects.select_related("medium").order_by(
            "-published_at", "guid"
        )
        if options["medium"]:
            articles = articles.filter(medium__slug=options["medium"])
        data = [
            {
                "medium": article.medium.slug,
                "guid": article.guid,
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "image_url": article.image_url,
                "published_at": article.published_at.isoformat(),
            }
            for article in articles
        ]
        options["path"].write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        self.stdout.write(f"Exported {len(data)} articles to {options['path']}")
