from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.db.models import CASCADE
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin



class UserRole(models.TextChoices):
    GUEST= "guest", _("Guest")
    HOST = "host", _("Host")
    ADMIN = "admin", _("Admin")


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        if role not in UserRole:
            raise ValueError("Invalid role")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, role="admin", password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, role, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=[("guest","Guest"),("host","Host"),("admin","Admin")], default="guest")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "user"
    class Meta:
        db_table='user'
        constraints=[
            models.UniqueConstraint(fields=["email"], name="unique_user_email")
            
        ]
        indexes=[
            models.Index(fields=["email"]),
            models.Index(fields=["user_id"])
        ]


class Conversation(models.Model):
    conversation_id=models.UUIDField(primary_key=True,editable=False, default=uuid.uuid4)
    participants=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"conversation {self.conversation_id}"


class Message(models.Model):
    message_id=models.UUIDField( max_length=50, editable=False,default=uuid.uuid4,primary_key=True)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE,related_name='sent_message')
    Conversation=models.ForeignKey(Conversation,on_delete=CASCADE, related_name="messages")
    message_body=models.TimeField()
    sent_at=models.DateField(default=timezone.now)

    def __str__(self):
        return f"message {self.message_id} from {self.sender}"










