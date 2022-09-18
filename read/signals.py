from traceback import print_tb
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ArtWork
from .utils import compress_image

@receiver(pre_save, sender=ArtWork)
def pre_save_artwork(sender, instance, **kwargs):
    print("Running art presave")
    if kwargs["raw"]:
        print("Raw detected skipped")
        return False
    print("Working")
    try:
        original_obj = ArtWork.objects.get(pk=instance.pk)
    except:
        instance.image = compress_image(instance.image, instance.title)
    else:
        if original_obj.image != instance.image:
            instance.image = compress_image(instance.image, instance.title)

