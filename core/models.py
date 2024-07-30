from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from words.models import Word


# Create your models here.
class Profile(AbstractUser):
    username = models.CharField(unique=True, verbose_name='شماره تلفن')
    password = models.CharField(max_length=128, verbose_name='رمز عبور')
    first_name = models.CharField(blank=True, null=True, max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='نام خانوادگی')
    # age = models.PositiveIntegerField(blank=True, null=True, verbose_name='سن')
    birth_date = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    membership = models.BooleanField(default=False, verbose_name='عضویت')
    liked_words = models.ManyToManyField(Word, blank=True, related_name='liked_by',
                                         verbose_name='کلمه های مورد علاقه')
    avatar = models.ImageField(blank=True, null=True, upload_to='uploads/',
                               validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='آواتار')

    def __str__(self):
        return str(self.username)
