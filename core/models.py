from django.db import models
from tinymce.models import HTMLField


class Masthead(models.Model):
    text = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.created_at} Masthead"

    def save(self, *args, **kwargs):
        if self.is_active:
            qs = type(self).objects.filter(is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(is_active=False)
        return super().save(*args, **kwargs)