from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from chats.models import User, Conversation, Message, UserRole

class Command(BaseCommand):
    help = "Populate the database with sample users, conversations, and messages"

    def handle(self, *args, **options):
        self.stdout.write("Populating database...")

        # --- Step 1: Create Users ---
        users_data = [
            {"email": "guest1@example.com", "first_name": "Guest", "last_name": "One", "role": UserRole.GUEST, "password": "123"},
            {"email": "guest2@example.com", "first_name": "Guest", "last_name": "Two", "role": UserRole.GUEST, "password": "123"},
            {"email": "host1@example.com", "first_name": "Host", "last_name": "One", "role": UserRole.HOST, "password": "123"},
            {"email": "admin1@example.com", "first_name": "Admin", "last_name": "One", "role": UserRole.ADMIN, "password": "123"},
        ]

        users = []
        for u in users_data:
            user, created = User.objects.get_or_create(
                email=u["email"],
                defaults={
                    "first_name": u["first_name"],
                    "last_name": u["last_name"],
                    "role": u["role"],
                }
            )
            if created:
                user.set_password(u["password"])
                user.save()
                self.stdout.write(f"Created user {user.email}")
            else:
                self.stdout.write(f"User {user.email} already exists")
            users.append(user)

        # --- Step 2: Create Conversations ---
        if len(users) >= 2:
            conv1 = Conversation.objects.create()
            conv1.participants.set(users[:2])  # guest1 + guest2
            conv1.save()
            self.stdout.write(f"Created conversation {conv1.conversation_id}")

            conv2 = Conversation.objects.create()
            conv2.participants.set(users[1:4])  # guest2 + host1 + admin1
            conv2.save()
            self.stdout.write(f"Created conversation {conv2.conversation_id}")

        # --- Step 3: Create Messages ---
        messages_text = [
            "Hello!",
            "How are you?",
            "This is a test message.",
            "Let's meet tomorrow.",
            "Goodbye!"
        ]

        conversations = Conversation.objects.all()
        for conv in conversations:
            for _ in range(5):  # 5 messages per conversation
                sender = random.choice(conv.participants.all())
                msg = Message.objects.create(
                    sender=sender,
                    conversation=conv,
                    message_body=random.choice(messages_text),
                    sent_at=timezone.now() - timedelta(days=random.randint(0, 10))
                )
                self.stdout.write(f"Created message {msg.message_id} from {sender.email}")

        self.stdout.write(self.style.SUCCESS("Database population complete!"))
