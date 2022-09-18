from django import template
from ..models import Ad
import random
register = template.Library()


@register.simple_tag
def get_ad(ad_type):
    return Ad.objects.filter(ad_type=ad_type, active=True).order_by("?").first()
    if random.random() > .5:
        ad = Ad.objects.filter(ad_type=ad_type, active=True).order_by("?").first()
    else:
        ad = None
    return ad