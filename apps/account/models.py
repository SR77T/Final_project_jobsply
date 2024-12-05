import uuid
from django.db import models
from apps.commons.models import DateTimeModel
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
    email = models.EmailField(max_length = 50, unique = True)
    middle_name = models.CharField(max_length = 50, null = True, blank = True)
    is_verified = models.BooleanField(default = False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()
    

class UserProfile(DateTimeModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_picture = models.FileField(null = True, blank = True, upload_to = "profile_pictures")
    phone_number = models.CharField(max_length= 14, null = True)
    address = models.CharField(max_length = 50)
    resume = models.FileField(null = True, blank = True, upload_to = "resumes")
    bio = models.TextField(max_length = 500)

    def __str__ (self):
        return f"Profile of {self.user.email}"


class UserAccountActivation(DateTimeModel):
    email = models.EmailField(max_length=50)
    key = models.CharField(max_length=100)

    def __str__(self):
        return f"key of {self.email}"