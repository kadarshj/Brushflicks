from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
#from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

ARTIST_CHOICES = (
    ('painter','Painter'),
    ('musician', 'Musician'),
    ('band','Band'),
    ('photography','Photography'),
    ('blogger','Blogger'),
)

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set or Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username="", **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(max_length=250,default='First Name')
    last_name = models.CharField(max_length=250,default='Last Name')
    i_like_being = models.CharField(max_length=25, choices=ARTIST_CHOICES, default='painter')
    my_pic = models.FileField(default='/my_image')
    # other fields...

    def __str__(self):
        return str(self.id) + ' - ' + str(self.user_id) + ' - ' + str(self.email_confirmed)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Artistshare(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    art_type = models.CharField(max_length=250)
    created_by = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    art_hidden = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,blank=True)
    like_count = models.IntegerField(default=0)
    flag_count = models.IntegerField(default=0)
    cover_logo = models.FileField()

    def __str__(self):
        return self.art_type + ' - ' + self.created_by


class Artliked(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    art = models.ForeignKey(Artistshare,on_delete=None)
    #like_created = models.DateTimeField(auto_now_add=True,blank=True)
    is_liked = models.BooleanField(default=False)
    is_notify = models.BooleanField(default=False)
    is_notify_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.art_id) + ' - ' + str(self.is_liked)


class Artflagged(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    art = models.ForeignKey(Artistshare,on_delete=None)
    is_flag_liked = models.BooleanField(default=False)
    is_flag_notify = models.BooleanField(default=False)
    is_flag_notify_read = models.BooleanField(default=False)
    flag_created = models.DateTimeField(auto_now_add=True,blank=True)


class Hire(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    hiring_skill = models.CharField(max_length=25, choices=ARTIST_CHOICES, default='painter')
    country = models.CharField(max_length=250)
    total_hour_work = models.IntegerField(default=0)
    budget = models.CharField(max_length=250)
    email_id = models.CharField(max_length=250)
    phone_no = models.CharField(max_length=25)
    skill_description = models.CharField(max_length=500)
    is_hired = models.BooleanField(default=False)
    hire_post_created = models.DateTimeField(auto_now_add=True)
    cover_logo = models.FileField()
    count_view = models.IntegerField(default=0)
    count_apply = models.IntegerField(default=0)

class Gethired(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    name = models.CharField(max_length=250)
    my_skill = models.CharField(max_length=25, choices=ARTIST_CHOICES, default='painter')
    country = models.CharField(max_length=250)
    hourly_charge = models.CharField(max_length=250)
    email_id = models.CharField(max_length=250)
    phone_no = models.CharField(max_length=25)
    personal_details = models.CharField(max_length=500)
    is_hired = models.BooleanField(default=False)
    gethire_post_created = models.DateTimeField(auto_now_add=True)
    cover_logo = models.FileField()
    count_view = models.IntegerField(default=0)
    count_interest = models.IntegerField(default=0)

class Hirereq(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    hire = models.ForeignKey(Hire,on_delete=None)
    name = models.CharField(max_length=250)
    email_id = models.CharField(max_length=250)
    phone_no = models.CharField(max_length=25)
    country = models.CharField(max_length=250)
    profession = models.CharField(max_length=250)
    remark = models.CharField(max_length=250)
    req_time = models.DateTimeField(auto_now_add=True)


class UserSample(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    art_album = models.CharField(max_length=250,default='Sample Album')
    music_album = models.CharField(max_length=250,default='Music Album')
    photo_album = models.CharField(max_length=250,default='Photo Album')
    song_title = models.CharField(max_length=250,default='Sample Song')
    music_type = models.CharField(max_length=250,default='Music Type')
    band_name = models.CharField(max_length=250,default='Band Name')
    blog_name = models.CharField(max_length=250)
    sample_blog = models.CharField(max_length=1500)
    sample_file = models.FileField()
    datetime = models.DateTimeField(auto_now_add=True)
    is_painter = models.BooleanField(default=False)
    is_photography = models.BooleanField(default=False)
    is_musician = models.BooleanField(default=False)
    is_band = models.BooleanField(default=False)
    is_blog = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user_id) + ' - ' + str(self.is_painter)


class Gethirereq(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    gethire = models.ForeignKey(Gethired,on_delete=None)
    name = models.CharField(max_length=250)
    email_id = models.CharField(max_length=250)
    phone_no = models.CharField(max_length=25)
    country = models.CharField(max_length=250)
    remark = models.CharField(max_length=500)
    req_time = models.DateTimeField(auto_now_add=True)


class Sellart(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    art_type = models.CharField(max_length=250)
    created_by = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    seller_name = models.CharField(max_length=250)
    total_count_product = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    art_sold_hidden = models.BooleanField(default=False)
    seller_email_id = models.CharField(max_length=250)
    seller_phone_number = models.IntegerField()
    seller_delivery_charge = models.FloatField(default=0.0)
    count_view = models.IntegerField(default=0)
    art_cover_logo = models.FileField()
    date = models.DateTimeField(auto_now_add=True)
    discount_price = models.IntegerField(default=0)
    country = models.CharField(max_length=100,default='India')


class SellProductAlbum(models.Model):
    user = models.ForeignKey(User,on_delete=None)
    sell = models.ForeignKey(Sellart,on_delete=None)
    album_files = models.FileField()
    upload_time = models.DateTimeField(auto_now_add=True)
    album_name = models.CharField(max_length= 250, default='Product Album')

    def __str__(self):
        return str(self.user_id) + ' - ' + str(self.sell_id)


class PreOrder(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    amount = models.IntegerField()
    buyer_name = models.CharField(max_length=250)
    shipping_street_address = models.CharField(max_length=500)
    shipping_country = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_pincode = models.IntegerField()
    phone = models.IntegerField()
    email = models.CharField(max_length=250)
    txnid = models.CharField(max_length=36, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)






