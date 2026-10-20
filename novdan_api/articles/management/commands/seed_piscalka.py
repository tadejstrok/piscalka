from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from ...models import Medium, MediumDonationAmount

SEED_DIR = Path(__file__).resolve().parents[2] / "seed_data"

MEDIUM_SLUG = "ppporocila"

DONATION_AMOUNTS = [
    (5, "Amorfna gmota", "amorfna-gmota.png"),
    (10, "Uporni kolesar", "uporni-kolesar.png"),
    (15, "Kaviar levičar", "kaviar-levicar.png"),
    (30, "Stric iz ozadja", "stric-iz-ozadja.png"),
]


class Command(BaseCommand):
    help = (
        "Create the Petkova Propagandna Poročila medium with its donation tiers. "
        "Used to build the static Piščalka site on a throwaway database."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--only",
            action="store_true",
            help="Delete all other media. Only use on a throwaway database.",
        )

    def handle(self, *args, **options):
        medium, created = Medium.objects.update_or_create(
            slug=MEDIUM_SLUG,
            defaults={
                "name": "Petkova Propagandna Poročila",
                "url": "https://www.youtube.com/@ppporocila",
                "article_rss_urls": "https://www.youtube.com/feeds/videos.xml?channel_id=UCUv0ELhovX1BZMmFDeSr6Rw",
                "donation_campaign_slug": MEDIUM_SLUG,
            },
        )
        self.stdout.write(f"{'Created' if created else 'Updated'} medium: {medium}")

        if options["only"]:
            deleted, _ = Medium.objects.exclude(pk=medium.pk).delete()
            self.stdout.write(f"Deleted {deleted} other objects")

        MediumDonationAmount.objects.filter(medium=medium).delete()
        for amount, name, filename in DONATION_AMOUNTS:
            donation_amount = MediumDonationAmount.objects.create(
                medium=medium,
                amount=amount,
                name=name,
                one_time=True,
                recurring=True,
            )
            content = (SEED_DIR / filename).read_bytes()
            donation_amount.image.save(filename, ContentFile(content), save=True)
            self.stdout.write(f"Created donation amount: {amount} {name}")
