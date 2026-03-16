from __future__ import annotations

from django.core.management.base import BaseCommand

from django_agent_rag.services import delete_document


class Command(BaseCommand):
    help = "Delete a document."

    def add_arguments(self, parser) -> None:
        parser.add_argument("document_id", type=int)
        parser.add_argument("--hard-delete", action="store_true")

    def handle(self, *args, **options):
        delete_document(options["document_id"], hard_delete=options["hard_delete"])
        self.stdout.write(self.style.SUCCESS("Document deleted"))

