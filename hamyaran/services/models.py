from django.db import models
from django.urls import reverse
from account.models import User, Address, FamilyMember
from django.utils import timezone
from extensions.utils import jalali_converter
from django_jalali.db.models import jDateField

# managers
class CategoryManager(models.Manager):
  def accessible(self):
    return self.filter(status=True)


class ServiceManager(models.Manager):
    def available(self):
        # Filter services where the related category's status is True
        return self.filter(category__status=True)


# Create your models here.
class Category(models.Model):
  title = models.CharField(max_length=100, verbose_name='دسته بندی')
  slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس')
  status = models.BooleanField(default=True, verbose_name='نمایش داده شود؟')
  position = models.IntegerField(verbose_name='پوزیشن')

  class Meta:
    verbose_name = 'دسته بندی'
    verbose_name_plural = 'دسته بندی ها'
    ordering = ('-position',)

  def __str__(self):
      return self.title
  
  objects = CategoryManager()    


class Service(models.Model):
  name = models.CharField(max_length=100, verbose_name='نام خدمت')
  category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name='دسته بندی', related_name='services')
  status = models.BooleanField(default=True, verbose_name='نمایش داده شود؟')
  cost = models.FloatField(verbose_name='قیمت')
  therapist = models.IntegerField(verbose_name='سهم درمانگر')

  class Meta:
    verbose_name = 'خدمت'
    verbose_name_plural = 'خدمات'
    ordering = ['name']

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("account:home")
    

  cats = ServiceManager()
  objects = CategoryManager()    


class Order(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='orders')
  service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name='خدمت')
  preferred_time = models.TimeField(null=True, blank=True ,verbose_name='زمان ترجیحی')
  special_condition = models.TextField(max_length=300, null=True, blank=True ,verbose_name='شرایط خاص')
  address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders', verbose_name='آدرس')
  order_for = models.ForeignKey(FamilyMember, null=True, blank=True, on_delete=models.CASCADE, related_name='orders', verbose_name='برای خودتان یا :')
  same_gender = models.BooleanField(default=True, verbose_name='درمانگر همجنس')
  created_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت سفارش')   
  order_date = jDateField(null=True, blank=True, verbose_name='انتخاب تاریخ')  

  def jcreated_time(self):
    return jalali_converter(self.created_time)
  jcreated_time.short_description = 'تاریخ سفارش'


  def __str__(self):
     return f"{self.service}"