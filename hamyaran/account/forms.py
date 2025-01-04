from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address, Pet, FamilyMember, Medicine
from services.models import Order
from django_jalali.forms import jDateField
from django_jalali.admin.widgets import AdminjDateWidget
    
    
class ProfileForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user')
    super(ProfileForm, self).__init__(*args, **kwargs)

    self.fields['username'].help_text = None
    
    if not user.is_superuser:
      self.fields['username'].disabled = True
      self.fields['email'].disabled = True
      self.fields['is_colleague'].disabled = True
      self.fields['special_user'].disabled = True 

  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'special_user', 'is_colleague', 'birthyear', 'birthmonth', 'birthday', 'phone', 'disease']

class BaseForm(forms.Form):
  pass

class SignupForm(UserCreationForm):
  email = forms.EmailField(max_length=200)

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['title', 'detail', 'location_link']
    widgets = {
      'detail': forms.Textarea(attrs={'rows': 3}),
    }

  def save(self, commit=True):
    # اطمینان از این که owner مقداردهی می‌شود
    instance = super().save(commit=False)
    if not instance.owner:
        instance.owner = self.initial.get('owner')
    if commit:
        instance.save()
    return instance

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'special_user', 'is_colleague', 'birthyear', 'birthmonth', 'birthday', 'phone', 'disease']

class PetForm(forms.ModelForm):
  class Meta:
    model = Pet
    fields = ['gender', 'name', 'type', 'race', 'birthyear', 'birthmonth', 'birthday']
 
  def save(self, commit=True):
    # اطمینان از این که owner مقداردهی می‌شود
    instance = super().save(commit=False)
    if not instance.owner:
        instance.owner = self.initial.get('owner')
    if commit:
        instance.save()
    return instance

class FamilyMemberForm(forms.ModelForm):
  class Meta:
    model = FamilyMember
    fields = ['gender', 'name', 'relation', 'phone', 'birthyear', 'birthmonth', 'birthday', 'disease']
 
  def save(self, commit=True):
    # اطمینان از این که owner مقداردهی می‌شود
    instance = super().save(commit=False)
    if not instance.parent:
        instance.parent = self.initial.get('parent')
    if commit:
        instance.save()
    return instance


class OrderForm(forms.ModelForm):

  class Meta:
    model = Order
    fields = [
      'service', 'preferred_time', 'special_condition', 'same_gender', 'address', 'order_for', 'order_date'
    ]

  order_date = jDateField(widget=AdminjDateWidget(attrs={'placeholder': 'با کلیک در این قسمت تاریخ را انتخاب کنید'}))
  order_date.label = 'تاریخ'      

  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None)
    super().__init__(*args, **kwargs)
    
    if user:
      self.fields['address'].queryset = Address.objects.filter(owner=user)
      self.fields['order_for'].queryset = FamilyMember.objects.filter(parent=user)

    self.fields['order_date'].lable = 'تاریخ'
    self.fields['service'].lable = 'خدمت'
    self.fields['preferred_time'].lable = 'زمان ترجیحی'
    self.fields['special_condition'].lable = 'شرایط خاص'
    self.fields['same_gender'].lable = 'درمانگر همجنس'
    self.fields['address'].lable = 'آدرس'

    self.fields['service'].widget.attrs.update({
      'placeholder': 'لطفا خدمت مورد نظر را انتخاب کنید'
    })
    self.fields['preferred_time'].widget.attrs.update({
      'placeholder': ' به صورت "16:00" بنویسید'
    })
    self.fields['special_condition'].widget.attrs.update({
      'placeholder': 'اگر بیمار یا محیط شرایط خاصی دارد که باید رعایت شود لطفا کامل شرح دهید'
    })
    self.fields['address'].widget.attrs.update({
      'placeholder': 'لطفا آدرس خود را از لیست آدرس هایی که در پروفایل ثبت کرده اید انتخاب کنید'
    })
    self.fields['same_gender'].widget.attrs.update({
      'placeholder': 'آیا ترجیح می دهید درمانگر باش ما همجنس باشد ؟'
    })