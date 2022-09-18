from os import access
from django.db import models
from django.db.models import Count
from datetime import datetime
from django.db.models import Q

class WorkManager(models.Manager):
    def get_trending(self):
        works = self.get_queryset().filter(active=True).filter(Q(views__created_at__date=datetime.today())).annotate(view_count=Count("views")).distinct().order_by("-view_count")[:3]
        if len(works) < 3:
            for i in range(3 - len(works)):
                works |= self.get_queryset().order_by("?")[:1]
        return works