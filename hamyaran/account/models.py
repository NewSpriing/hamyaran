from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from extensions.utils import jalali_converter, age, birth_day
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User(AbstractUser):
  MONTH_CHOICES = [
  ('فروردین', 'فروردین'),
  ('اردیبهشت', 'اردیبهشت'),
  ('خرداد', 'خرداد'),
  ('تیر', 'تیر'),
  ('مرداد', 'مرداد'),
  ('شهریور', 'شهریور'),
  ('مهر', 'مهر'),
  ('آبان', 'آبان'),
  ('آذر', 'آذر'),
  ('دی', 'دی'),
  ('بهمن', 'بهمن'),
  ('اسفند', 'اسفند'),
]

  GENDER_CHOICES = [('زن','زن'),('مرد','مرد')]

  DISEASE_CHOICES = [
    ('دیابت', 'دیابت'),
    ('سرطان', 'سرطان'),
    ('بیماری قلبی', 'بیماری قلبی'),
    ('فشار خون', 'فشار خون'),
    ('بیماری های ریوی', 'بیماری های ریوی'),
    ('نارسایی کلیه', 'نارسایی کلیه'),
    ('کم خونی', 'کم خونی'),
    ('بیماری های مادرزادی', 'بیماری های مادرزادی'),
    ('مشکلات کبدی و گوارشی', 'مشکلات کبدی و گوارشی'),
    ('سایر', 'سایر'),
  ]

  email = models.EmailField(unique=True, verbose_name='پست الکترونیکی')
  is_staff = models.BooleanField(default=False, verbose_name='وضعیت کارمندی')
  is_active = models.BooleanField(default=True, verbose_name='وضعیت فعالیت')
  is_colleague = models.BooleanField(default=False, verbose_name='وضعیت همکاری')
  special_user = models.DateTimeField(default=timezone.now, verbose_name='کاربر ویژه تا')
  created_time = models.DateTimeField(default=timezone.now, verbose_name='عضویت')
  birthyear = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1300),MaxValueValidator(1450)] ,verbose_name='سال تولد')
  birthmonth = models.CharField(null=True, blank=True, max_length=15, choices=MONTH_CHOICES, verbose_name='ماه تولد')
  birthday = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1),MaxValueValidator(31)] ,verbose_name='روز تولد')
  phone = models.CharField(null=True, blank=True, max_length=15, verbose_name='شماره همراه', unique=True)
  gender = models.CharField(null=True, blank=True, max_length=3, choices=GENDER_CHOICES, verbose_name='جنسیت')
  disease = models.CharField(null=True, blank=True, max_length=100, choices=DISEASE_CHOICES, verbose_name='بیماری های زمینه ای')
  subscription_info = models.JSONField(null=True, blank=True)


  def is_special_user(self):
    if self.special_user > timezone.now():
      return "بله"
    else :
      return "خیر"  
  is_special_user.Boolean = True    
  is_special_user.short_description = 'کاربر ویژه'

  def jspecial_user(self):
    return jalali_converter(self.special_user)
  jspecial_user.short_description = 'تا تاریخ'

  def jcreated_time(self):
    return jalali_converter(self.created_time)
  jcreated_time.short_description = 'تاریخ عضویت'

  def age(self):
    return age(self.birthyear, self.birthmonth, self.birthday)
  age.short_description = 'سن'

  def is_birth_day(self):
    return birth_day(self.birthyear, self.birthmonth, self.birthday)
  is_birth_day.short_description = 'تولد'  

  def __str__(self):
    return self.get_full_name()

class Address(models.Model):
  title = models.CharField(max_length=200, verbose_name='عنوان')
  detail = models.TextField(verbose_name='جزئیات')
  owner = models.ForeignKey(User ,on_delete=models.CASCADE, verbose_name='مالک آدرس', related_name="addresses")
  location_link = models.URLField(null=True, blank=True ,verbose_name='لینک گوگل مپ')

  class Meta:
    verbose_name = 'آدرس'
    verbose_name_plural = 'آدرس  ها'

  def __str__(self):
    return self.title

class Pet(models.Model):

  MONTH_CHOICES = [
  ('فروردین', 'فروردین'),
  ('اردیبهشت', 'اردیبهشت'),
  ('خرداد', 'خرداد'),
  ('تیر', 'تیر'),
  ('مرداد', 'مرداد'),
  ('شهریور', 'شهریور'),
  ('مهر', 'مهر'),
  ('آبان', 'آبان'),
  ('آذر', 'آذر'),
  ('دی', 'دی'),
  ('بهمن', 'بهمن'),
  ('اسفند', 'اسفند'),
]

  GENDER_CHOICES = [('دختر','دختر'),('پسر','پسر')]

  TYPE_CHOICES = [('سگ', 'سگ'), ('گربه', 'گربه'), ('خزنده', 'خزنده'), ('پرنده', 'پرنده'), ('جونده', 'جونده'), ('آبزی', 'آبزی'), ('سایر', 'سایر')]

  name = models.CharField(max_length=100, verbose_name='نام پت')
  owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='صاحب', related_name='pets')
  gender = models.CharField(max_length=4, choices=GENDER_CHOICES, verbose_name='جنسیت')
  type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='گونه')
  race = models.CharField(max_length=40, verbose_name='نژاد')
  birthyear = models.IntegerField(validators=[MinValueValidator(1300),MaxValueValidator(1450)] ,verbose_name='سال تولد')
  birthmonth = models.CharField(max_length=15, choices=MONTH_CHOICES, verbose_name='ماه تولد')
  birthday = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(31)] ,verbose_name='روز تولد')

  class Meta:
    verbose_name = 'پت'
    verbose_name_plural = 'پت  ها'

  def age(self):
    return age(self.birthyear, self.birthmonth, self.birthday)
  age.short_description = 'سن'

  def is_birth_day(self):
    return birth_day(self.birthyear, self.birthmonth, self.birthday)
  is_birth_day.short_description = 'تولد' 

  def __str__(self):
    return f"{self.name} - {self.type} - {self.race}"

class FamilyMember(models.Model):

  MONTH_CHOICES = [
  ('فروردین', 'فروردین'),
  ('اردیبهشت', 'اردیبهشت'),
  ('خرداد', 'خرداد'),
  ('تیر', 'تیر'),
  ('مرداد', 'مرداد'),
  ('شهریور', 'شهریور'),
  ('مهر', 'مهر'),
  ('آبان', 'آبان'),
  ('آذر', 'آذر'),
  ('دی', 'دی'),
  ('بهمن', 'بهمن'),
  ('اسفند', 'اسفند'),
]

  GENDER_CHOICES = [('زن','زن'),('مرد','مرد')]

  DISEASE_CHOICES = [
    ('دیابت', 'دیابت'),
    ('سرطان', 'سرطان'),
    ('بیماری قلبی', 'بیماری قلبی'),
    ('فشار خون', 'فشار خون'),
    ('بیماری های ریوی', 'بیماری های ریوی'),
    ('نارسایی کلیه', 'نارسایی کلیه'),
    ('کم خونی', 'کم خونی'),
    ('بیماری های مادرزادی', 'بیماری های مادرزادی'),
    ('مشکلات کبدی و گوارشی', 'مشکلات کبدی و گوارشی'),
    ('سایر', 'سایر'),
  ]

  name = models.CharField(max_length=50, verbose_name='نام')
  relation = models.CharField(max_length=50, verbose_name='نسبت')
  parent = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='والد', related_name='family_members')
  created_time = models.DateTimeField(default=timezone.now, verbose_name='عضویت')
  birthyear = models.IntegerField(validators=[MinValueValidator(1300),MaxValueValidator(1450)] ,verbose_name='سال تولد')
  birthmonth = models.CharField(max_length=15, choices=MONTH_CHOICES, verbose_name='ماه تولد')
  birthday = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(31)] ,verbose_name='روز تولد')
  phone = models.IntegerField(verbose_name='شماره همراه')
  gender = models.CharField(max_length=3, choices=GENDER_CHOICES, verbose_name='جنسیت')
  disease = models.CharField(null=True, blank=True, max_length=100, choices=DISEASE_CHOICES, verbose_name='بیماری های زمینه ای')

  class Meta:
    verbose_name = 'عضو'
    verbose_name_plural = 'اعضا'

  def jcreated_time(self):
    return jalali_converter(self.created_time)
  jcreated_time.short_description = 'تاریخ عضویت'

  def age(self):
    return age(self.birthyear, self.birthmonth, self.birthday)
  age.short_description = 'سن'

  def is_birth_day(self):
    return birth_day(self.birthyear, self.birthmonth, self.birthday)
  is_birth_day.short_description = 'تولد'  

  def __str__(self):
    return self.name

class Notification(models.Model):
  recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='گیرنده')
  message = models.TextField(verbose_name='پیام')
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ:')
  is_read = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.recipient} at {self.created_at}"

  def jcreated_at(self):
    return jalali_converter(self.created_at)
  jcreated_at.short_description = 'تاریخ پیام'  

class Medicine(models.Model):
    USEAGE_CHOICES = [
      ('موضعی', 'موضعی'),
      ('خوراکی', 'خوراکی'),
      ('تزریقی', 'تزریقی'),
      ('مقعدی', 'مقعدی'),
      ('سایر', 'سایر'),
    ]
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="ایجاد کننده دارو")
    name = models.CharField(max_length=255, verbose_name="نام دارو")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات دارو")
    dose = models.CharField(max_length=50, verbose_name="دوز مصرف")  # مانند 1 قرص، 2 میلی‌لیتر
    useage_way = models.CharField(max_length=50, choices=USEAGE_CHOICES, verbose_name="نحوه مصرف") 
    is_active = models.BooleanField(default=True, verbose_name="فعال")  # برای فعال/غیرفعال کردن یادآوری
    created_at = models.DateTimeField(auto_now_add=True)

    def jcreated_at(self):
      return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد دارو'  

    def __str__(self):
        return self.name

class Prescription(models.Model):
    prescribed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="prescribed_by", verbose_name="تجویز کننده")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_prescriptions", verbose_name="مصرف کننده")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name="دارو")
    interval = models.PositiveIntegerField(verbose_name="فاصله زمانی مصرف")  # زمان بین هر دوز
    qty = models.PositiveIntegerField(null=True, blank=True, verbose_name=" تعداد مصرف")  # تعداد مصرف
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="زمان شروع")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def jstart_date(self):
      return jalali_converter(self.start_date)
    jstart_date.short_description = 'زمان شروع دارو'      

    def jcreated_at(self):
      return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد نسخه'  

    def user_full_name(self):
      return self.user.get_full_name()

    def __str__(self):
        return f"{self.medicine.name} for {self.user.username}"

class Reminder(models.Model):
  prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="reminders", verbose_name="نسخه")
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مصرف کننده")
  reminder_time = models.DateTimeField(verbose_name="زمان یادآوری")
  is_read = models.BooleanField(default=False, verbose_name="مصرف شده")
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
  device_id = models.CharField(max_length=255, blank=True, null=True)

  def jcreated_at(self):
    return jalali_converter(self.created_at)
  jcreated_at.short_description = 'تاریخ ایجاد '  

  def jreminder_time(self):
    return jalali_converter(self.reminder_time)
  jreminder_time.short_description = 'زمان مصرف '  

  def __str__(self):
      return f"Reminder for {self.user.username} at {self.reminder_time}"

class WebPushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    endpoint = models.URLField()
    auth_key = models.CharField(max_length=255)
    p256dh_key = models.CharField(max_length=255)
