from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from mindspace.models import *
from .models import Notification
from qna.models import Answer

@receiver(post_save, sender=ShareMindspace)
def create_notif_share_mindspace(sender, instance, **kwargs):
    if instance.access_level == sender.editor:
        notification_type = Notification.ADD_EDITOR
    # elif instance.access_level == sender.commenter:
    #     notification_type = Notification.ADD_COMMENTER
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
    # elif instance.access_level == sender.commenter:
    #     notification_type = Notification.REMOVE_COMMENTER
    else:
        notification_type = Notification.REMOVE_VIEWER
    
    n = Notification.objects.create(
        sent_by=instance.shared_by,
        received_by=instance.shared_with,
        notification_type=notification_type,
        subject_mindspace=instance.mindspace
    )

# @receiver(m2m_changed, sender=Mindspace.editors.through)
# def create_notification_mindspace_editor(sender, instance, action, **kwargs):
#     received_by = kwargs['model'].objects.get(id=list(kwargs['pk_set'])[0])
#     if action == 'post_add':
#         n = Notification.objects.create(
#             sent_by=instance.owner,
#             received_by=received_by,
#             notification_type=Notification.ADD_EDITOR,
#             subject_mindspace=instance
#         )
#     elif action == 'post_remove':
#         n = Notification.objects.create(
#             sent_by=instance.owner,
#             received_by=received_by,
#             notification_type=Notification.REMOVE_EDITOR,
#             subject_mindspace=instance
#         )

# @receiver(m2m_changed, sender=Mindspace.commenters.through)
# def create_notification_mindspace_commenter(sender, instance, action, created, **kwargs):
#     received_by = kwargs['model'].objects.get(id=list(kwargs['pk_set'])[0])
#     if action == 'post_add':
#         n = Notification.objects.create(
#             sent_by=instance.owner,
#             received_by=received_by,
#             notification_type=Notification.ADD_COMMENTER,
#             subject_mindspace=instance
#         )
#     elif action == 'post_remove':
#         n = Notification.objects.create(
#             sent_by=instance.owner,
#             received_by=received_by,
#             notification_type=Notification.REMOVE_COMMENTER,
#             subject_mindspace=instance
#         )

# @receiver(m2m_changed, sender=Mindspace.viewers.through)
# def create_notification_mindspace_viewer(sender, instance, action, created, **kwargs):
#     received_by = kwargs['model'].objects.get(id=list(kwargs['pk_set'])[0])
#     text = ''
#     if action == 'post_add':
#         n = Notification.objects.create(
#             sent_by=instance.owner,
#             received_by=received_by,
#             notification_type=Notification.ADD_VIEWER,
#             subject_mindspace=instance
#         )
#     elif action == 'post_remove':
#         n = Notification.objects.create(
#             sent_by=instance.owner,
#             received_by=received_by,
#             notification_type=Notification.REMOVE_VIEWER,
#             subject_mindspace=instance
#         )

@receiver(post_save, sender=Answer)
def create_notification_question_answered(sender, instance, created, **kwargs):
    received_by = instance.question.owner
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