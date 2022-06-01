from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from mindspace.models import *
from .models import Notification
from qna.models import Answer

@receiver(post_save, sender=ShareMindspace)
def create_notif_share_mindspace(sender, instance, **kwargs):
    if instance.access_level == sender.editor:
        notification_type = Notification.ADD_EDITOR
    else:
        notification_type = Notification.ADD_VIEWER
    
    n = Notification.objects.create(
        sent_by=instance.shared_by,
        received_by=instance.shared_with,
        notification_type=notification_type,
        subject_mindspace=instance.mindspace
    )

@receiver(post_delete, sender=ShareMindspace)
def create_notif_share_mindspace_remove(sender, instance, **kwargs):
    if instance.access_level == sender.editor:
        notification_type = Notification.REMOVE_EDITOR
    else:
        notification_type = Notification.REMOVE_VIEWER
    
    n = Notification.objects.create(
        sent_by=instance.shared_by,
        received_by=instance.shared_with,
        notification_type=notification_type,
        subject_mindspace=instance.mindspace
    )

@receiver(post_save, sender=Answer)
def create_notification_question_answered(sender, instance, created, **kwargs):
    received_by = instance.question.owner
    if instance.owner != received_by:
        if created:
            notification_type = Notification.POST_ANSWER
        else:
            notification_type = Notification.UPDATE_ANSWER

        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=notification_type,
            subject_answer=instance
        )