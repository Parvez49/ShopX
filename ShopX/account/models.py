from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

from common.base_model import BaseModelWithUID
from account.managers import CustomUserManager
import secrets
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField


class User(BaseModelWithUID, AbstractBaseUser, PermissionsMixin):
    slug = AutoSlugField(populate_from="get_full_name", unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = PhoneNumberField(
        blank=True, unique=True, db_index=True, verbose_name="Phone Number"
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    referral_code = models.CharField(max_length=8, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.phone

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_referral_code(length):
        alphabet = "0123456789"
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def generate_unique_referral_code(self):
        code_length = 8
        code = self.generate_referral_code(code_length)

        while User.objects.filter(referral_code=code).exists():
            code = self.generate_referral_code(code_length)

        return code
