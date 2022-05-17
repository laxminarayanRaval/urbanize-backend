import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """
    Creating a manager for a custom user model
    """

    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username, and password.
        """
        if not email:
            raise ValueError('User Must have an Email Address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Create and return a User with Superuser (admin) Permissions.
        """
        if password is None:
            raise TypeError('Superuser must have a password.')
        user = self.create_user(email, password)
        user.role = 1
        user.save()

        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, uuid=uuid.uuid4)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=25, choices=(('admin', 'Admin'), ('user', 'User'), ('prof', 'Professional')),
                            default='user')
    DOB = models.DateTimeField(null=True)
    gender = models.CharField(max_length=25, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Others')))
    profile_pic_url = models.CharField(max_length=255,
                                       default='https://res.cloudinary.com/urban-solutions/image/upload/v1652793543/icon-1633249_960_720_ae71g3.png')

