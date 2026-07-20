from django.db import models
from django.utils import timezone

from apps.common.managers import ActiveManager, AllObjectsManager, DeletedManager

class SoftDeleteModel(models.Model):

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()
    deleted_objects = DeletedManager()
    all_objects = AllObjectsManager()

    def delete(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save(update_fields=['is_deleted', 'deleted_at'])


    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.deleted_at = None
            self.save(update_fields=['is_deleted', 'deleted_at'])


    def hard_delete(self):
        super().delete()

    class Meta:
        abstract = True