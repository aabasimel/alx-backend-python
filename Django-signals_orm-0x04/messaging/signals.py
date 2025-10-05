"""Module imports for messaging.signals"""

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory


User = get_user_model()


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal handler that creates a notification when a new message is sent.
    """
    if created:
        notification_content = (
            f"New message from {instance.sender.username}: {instance.content[:50]}"
        )

        if len(instance.content) > 50:
            notification_content += "..."

        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type="message",
            content=notification_content,
        )

        print(f"Notification created for {instance.receiver.username}")


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal handler that logs messages.
    """
    if not instance.pk:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message, old_content=old_message.content
        )
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_related_data(sender, instance, **kwargs):
    """
    After a User is deleted, ensure all related objects are cleaned up.
    CASCADE will handle most of it, but this ensures no leftovers.
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    Notification.objects.filter(user=instance).delete()

    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()