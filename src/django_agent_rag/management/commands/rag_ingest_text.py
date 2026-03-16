from __future__ import annotations

import json

from django.core.management.base import BaseCommand

from django_agent_rag.services import ingest_text


class Command(BaseCommand):
    help = "Ingest raw text into the RAG store."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--title", required=True)
        parser.add_argument("--text", required=True)
        parser.add_argument("--external-id", default="")
        parser.add_argument("--metadata", default="{}")

    def handle(self, *args, **options):
        document = ingest_text(
            title=options["title"],
            text=options["text"],
            external_id=options["external_id"],
            metadata=json.loads(options["metadata"]),
        )
        self.stdout.write(self.style.SUCCESS(f"Ingested document {document.id}"))

