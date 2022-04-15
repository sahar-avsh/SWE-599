from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from mindspace.models import *
from .models import Notification
from qna.models import Answer

@receiver(m2m_changed, sender=Mindspace.editors.through)
def create_notification_mindspace_editor(sender, instance, action, **kwargs):
    received_by = kwargs['model'].objects.get(id=list(kwargs['pk_set'])[0])
    if action == 'post_add':
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.ADD_EDITOR,
            subject_mindspace=instance
        )
    elif action == 'post_remove':
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.REMOVE_EDITOR,
            subject_mindspace=instance
        )

@receiver(m2m_changed, sender=Mindspace.commenters.through)
def create_notification_mindspace_commenter(sender, instance, action, created, **kwargs):
    received_by = kwargs['model'].objects.get(id=list(kwargs['pk_set'])[0])
    if action == 'post_add':
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.ADD_COMMENTER,
            subject_mindspace=instance
        )
    elif action == 'post_remove':
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.REMOVE_COMMENTER,
            subject_mindspace=instance
        )

@receiver(m2m_changed, sender=Mindspace.viewers.through)
def create_notification_mindspace_viewer(sender, instance, action, created, **kwargs):
    received_by = kwargs['model'].objects.get(id=list(kwargs['pk_set'])[0])
    text = ''
    if action == 'post_add':
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.ADD_VIEWER,
            subject_mindspace=instance
        )
    elif action == 'post_remove':
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.REMOVE_VIEWER,
            subject_mindspace=instance
        )

@receiver(post_save, sender=Answer)
def create_notification_question_answered(sender, instance, created, **kwargs):
    received_by = instance.question.owner
    if created:
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.POST_ANSWER,
            subject_answer=instance
        )
    else:
        n = Notification.objects.create(
            sent_by=instance.owner,
            received_by=received_by,
            notification_type=Notification.UPDATE_ANSWER,
            subject_answer=instance
        )