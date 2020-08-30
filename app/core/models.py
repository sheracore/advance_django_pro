from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
# This is recommended way to retrieve defferent setting from the django setting file              
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **exrea_fields):
        """ Create and saves a new user """
        if not email:
            raise ValueError('Useres most have an email address')
        user = self.model(email=self.normalize_email(email), **exrea_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ create and saves a new supers uer """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that suppors using email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for recipe"""
    name = models.CharField(max_length=255)
    # Now we want to connect to User model so we can connect by foreign key but 
    # in there the best practice are using settings to retrieve our auth user model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return self.name