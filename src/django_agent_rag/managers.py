from django.db import models


class DocumentQuerySet(models.QuerySet):
    def active(self) -> "DocumentQuerySet":
        return self.exclude(status="deleted")


class DocumentManager(models.Manager):
    def get_queryset(self) -> DocumentQuerySet:
        return DocumentQuerySet(self.model, using=self._db)

