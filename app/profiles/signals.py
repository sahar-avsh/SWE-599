from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from mindspace.models import *
from .models import Notification
from qna.models import Answer, Activity

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
        subject_mindspace=instance.shared_mindspace
    )

@receiver(pre_delete, sender=ShareMindspace)
def create_notif_share_mindspace_remove(sender, instance, **kwargs):
    if instance.access_level == sender.editor:
        notification_type = Notification.REMOVE_EDITOR
    else:
        notification_type = Notification.REMOVE_VIEWER
    
    n = Notification.objects.create(
        sent_by=instance.shared_by,
        received_by=instance.shared_with,
        notification_type=notification_type,
        subject_mindspace=instance.shared_mindspace
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

@receiver(post_save, sender=Activity)
def create_notification_vote_add(sender, instance, created, **kwargs):
    sent_by = instance.owner
    if instance.activity_type == 'U':
        notification_type = Notification.UP_VOTE
    else:
        notification_type = Notification.DOWN_VOTE

    n = Notification.objects.create(
        sent_by=sent_by,
        received_by=instance.answer.owner,
        notification_type=notification_type,
        subject_answer=instance.answer
    )

@receiver(pre_delete, sender=Activity)
def create_notif_vote_remove(sender, instance, **kwargs):
    notification_type = Notification.TAKE_VOTE
    
    n = Notification.objects.create(
        sent_by=instance.owner,
        received_by=instance.answer.owner,
        notification_type=notification_type,
        subject_answer=instance.answer
    )