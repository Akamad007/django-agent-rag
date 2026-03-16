from __future__ import annotations

from django.core.management.base import BaseCommand

from django_agent_rag.models import AgentRun, Chunk, Document, RetrievalRun


class Command(BaseCommand):
    help = "Show package statistics."

    def handle(self, *args, **options):
        self.stdout.write(f"Documents: {Document.objects.count()}")
        self.stdout.write(f"Chunks: {Chunk.objects.count()}")
        self.stdout.write(f"Retrieval runs: {RetrievalRun.objects.count()}")
        self.stdout.write(f"Agent runs: {AgentRun.objects.count()}")

