# import json
#
# from django.dispatch import receiver
# from django.db.models.signals import post_save
#
# from kirisame.models.toot import Toot
# from kirisame.tasks import download_artwork
#
#
# @receiver(post_save, sender=Toot)
# def schedule_toot(sender, instance, created, **kwargs):
#     # Навешать FSM
#     if not instance.file_names:
#         download_artwork.apply_async((json.loads(instance.image_urls), instance.id), queue='downloads')
