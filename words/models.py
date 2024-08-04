from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.db import models



class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان دسته بندی')
    image = models.ImageField(blank=True, null=True, upload_to='uploads/',
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                              verbose_name='تصویر دسته بندی')
    parent = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='children',
                               verbose_name='دسته بندی پدر')

    def __str__(self):
        return self.title


class Word(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان کلمه')
    explanation = models.TextField(blank=True, null=True, verbose_name='توضیحات کلمه')
    image = models.ImageField(blank=True, null=True, upload_to='uploads/',
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                              verbose_name='تصویر')
    video = models.FileField(blank='True', null='True', upload_to='uploads/',
                             validators=[FileExtensionValidator(['mp4', 'mkv'])], verbose_name='ویدیو')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='words',
                                 verbose_name='دسته بندی')
    slug = models.SlugField(unique=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
