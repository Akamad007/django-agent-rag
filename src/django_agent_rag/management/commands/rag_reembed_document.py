from __future__ import annotations

from django.core.management.base import BaseCommand

from django_agent_rag.services import embed_document


class Command(BaseCommand):
    help = "Re-embed all chunks for a document."

    def add_arguments(self, parser) -> None:
        parser.add_argument("document_id", type=int)

    def handle(self, *args, **options):
        chunks = embed_document(options["document_id"])
        self.stdout.write(self.style.SUCCESS(f"Updated {len(chunks)} chunks"))

