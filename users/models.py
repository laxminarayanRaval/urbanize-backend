import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


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
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    role = models.CharField('User Role', max_length=25,
                            choices=(('user', 'User'), ('prof', 'Professional'), ('admin', 'Admin'),),
                            default='user')
    full_name = models.CharField('Full Name', max_length=30, null=False)
    date_of_birth = models.DateTimeField('Date of Birth', null=True)
    gender = models.CharField(max_length=25, choices=(
        ('male', 'Male'), ('female', 'Female'), ('other', 'Others')), default='male')
    profile_pic_url = models.URLField(null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    mobile_no = models.CharField('User Contact No.', null=True, max_length=20)
    date_joined = models.DateTimeField('date account created', auto_now_add=True)
    date_updated = models.DateTimeField('date account updated', auto_now=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self): return str(self.email)


class Service(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    service_name = models.CharField('Service Category', max_length=50, null=False, unique=True)
    description = models.CharField('Service Category Description', max_length=255, null=True)
    img_url = models.URLField('Service Img URL', null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self): return str(self.service_name)


class SubService(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    service_name = models.CharField('Sub-Service Category', max_length=30, null=False, unique=True)
    description = models.CharField('Sub-Service Category Description', max_length=255, null=True)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    img_url = models.URLField('Service Img URL', null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self): return f'{self.service_name} of {self.service_id}'


class ProfessionalUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # cities = models.CharField('Listing in Cities', max_length=255, null=False)
    cities = ArrayField(models.CharField(max_length=25), default=list)
    # availability_hours = models.CharField('Service Timing', max_length=50, null=True)
    startsTime = models.TimeField(verbose_name="Availability Start Time", null=False)
    endsTime = models.TimeField(verbose_name='Availability End Time', null=False)
    address = models.CharField('Office Address', max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self): return f'{self.user_id} provides services in ({self.cities})'


class ProfessionalUserService(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    prof_id = models.ForeignKey(ProfessionalUser, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    subservice_ids = ArrayField(models.CharField(max_length=255, null=True))
    description = models.TextField(null=True)
    proof_img_url = models.URLField('Proof Image', null=False)
    charges = models.FloatField('Cost for Service', null=True)
    estimate_time = models.CharField('Time to Complete', max_length=255, null=True)
    payment_modes = ArrayField(models.CharField(max_length=30, default='cash'))
    is_active = models.BooleanField(default=True)

    def __str__(self): return f'{self.prof_id} provides service {self.service_id},\
    completes task in {self.estimate_time} with charges of {self.charges}'


class Reviews(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    prof_serv_id = models.ForeignKey(ProfessionalUserService, on_delete=models.CASCADE)
    start_counts = models.FloatField('Start Ratings', null=False)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self): return f'{self.user_id} got {self.start_counts} Stars in {self.prof_serv_id} service'


class ProfessionalUserServiceImages(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    prof_serv_id = models.ForeignKey(ProfessionalUserService, on_delete=models.CASCADE)
    img_urls = models.URLField('Uploaded Images URL', null=False)


class ContactUsQuery(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_("Email Address"), max_length=255)
    mobile = models.CharField(_("Phone Number"), max_length=255)
    title = models.CharField(_("Title"), max_length=255)
    desc = models.CharField(_("Dec. Message"), max_length=255)
    is_active = models.BooleanField(default=True)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField('date query made', auto_now=True)
    updated_at = models.DateTimeField('date update made', auto_now=True)

    def __str__(self):
        return f'{self.title} : {self.first_name}'


class UserRequirement(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subservice_id = models.ForeignKey(SubService, on_delete=models.CASCADE)
    descriptive_msg = models.TextField()
    interested_prof = ArrayField(models.CharField(max_length=25), default=list)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date query made', auto_now_add=True)
    updated_at = models.DateTimeField('date update made', auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'UserRequirement : {self.created_by} on {self.created_at}'

# class HireProfessionalRequest(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#     prof_id = models.ForeignKey(ProfessionalUserService, on_delete=models.CASCADE)
#     # subservice_id = models.ForeignKey(SubService, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     hire_date = models.DateField(null=True, blank=True)
#     descriptive_msg = models.TextField(null=True)
#     status = models.CharField(max_length=25, choices=(
#         ('pending', 'Pending'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted'), ('rejected', 'Rejected'),
#         ('completed', 'Completed')), default='pending')
#     created_at = models.DateTimeField('date query made', auto_now_add=True)
#     updated_at = models.DateTimeField('date update made', auto_now=True)
#


class FlaggedProfessionalUserReport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    prof_id = models.ForeignKey(ProfessionalUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date query made', auto_now_add=True)
    updated_at = models.DateTimeField('date update made', auto_now=True)


class FavouriteUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    prof_id = models.ForeignKey(ProfessionalUser, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date query made', auto_now_add=True)
    updated_at = models.DateTimeField('date update made', auto_now=True)
