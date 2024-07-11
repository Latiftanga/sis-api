from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class Person(models.Model):
    """Person abstract model"""
    first_name = models.CharField(max_length=32)
    other_names = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=1)
    date_of_birth = models.DateField(blank=True)
    mobile_phone = models.CharField(
      max_length=32, blank=True, default=''
    )
    email = models.EmailField(
      max_length=64,
      blank=True,
      default=''
    )
    religion = models.CharField(
      max_length=32, blank=True, default=''

    )
    nationality = models.CharField(max_length=128)
    national_id = models.CharField(
      max_length=32, blank=True, default=''
    )
    social_security_no = models.CharField(
      max_length=32, blank=True, default=''
    )

    class Meta:
        abstract = True


class Address(models.Model):
    """Person address"""
    CATEGORIES = (
        ('Resemailential', 'Resemailential'),
        ('Work', 'Work'),
        ('Permanent', 'Permanent')
    )
    category = models.CharField(max_length=32, choices=CATEGORIES)
    location = models.CharField(max_length=128)
    building_no = models.CharField(
        max_length=32, blank=True, default=''
    )
    city = models.CharField(max_length=128)
    region = models.CharField(max_length=64)
    postal_code = models.CharField(
        max_length=32, blank=True, default=''
    )
    digital_code = models.CharField(
        max_length=32, blank=True, default=''
    )

    def __str__(self):
        return f'{self.location}, {self.city}, {self.region}'


class UserManager(BaseUserManager):
    """"Manage for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_adminuser(self, email, password):
        """Create and return a new admin user"""
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_teacheruser(self, email, password):
        """Create and return a new teacher user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_studentuser(self, email, password):
        """Create and return a new student user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_guardianuser(self, email, password):
        """Create and return a new guardian user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
