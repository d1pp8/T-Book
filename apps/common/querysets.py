from django.db import models
from django.utils import timezone

class SoftDeleteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

    def only_deleted(self):
        return self.filter(is_deleted=True)

    def delete(self):
        return self.active().update(is_deleted=True, deleted_at=timezone.now())

    def restore(self):
        return self.update(is_deleted=False, deleted_at=None)

    def hard_delete(self):
        return super().delete()

