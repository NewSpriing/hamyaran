from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.db.models import Min
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from push_notifications.models import GCMDevice
from datetime import timedelta
from typing import cast
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from services.models import Service, Category
from .tokens import account_activation_token
from .forms import ProfileForm, SignupForm, AddressForm, UserForm, PetForm, FamilyMemberForm
from .models import User, Address, Notification, Medicine, Prescription, Reminder, Pet, FamilyMember, WebPushSubscription
from .mixins import FieldsMixin, EditAccessMixin, SuperUserAccessMixin, ColleagueRequiredMixin, UserContextMixin

# Create your views here.
class ServiceList(LoginRequiredMixin, ListView):
  model = Service
#  queryset = Service.objects.filter(status=True)
  template_name = 'registration/home.html'
  
  def get_queryset(self):
    user = cast(User, self.request.user)
    if user.is_superuser:  
      return Service.objects.all()
    else:
      return Service.objects.accessible()

class ServiceCreate(LoginRequiredMixin, FieldsMixin, CreateView):
  model = Service
  template_name = 'registration/service-create-update.html'

class ServiceUpdate(EditAccessMixin, FieldsMixin, UpdateView):
  model = Service
  template_name = 'registration/service-create-update.html'

class ServiceDelete(SuperUserAccessMixin, DeleteView):
  model = Service
  success_url = reverse_lazy('account:home')  
  
def category(request, slug):
  context = {
   'category' : get_object_or_404(Category, slug=slug, status=True)
  }
  return render(request, 'registration/categories.html', context)

class Profile(LoginRequiredMixin, UpdateView, UserContextMixin):
  model = User
  template_name = 'registration/profile.html'
  form_class = ProfileForm
  success_url = reverse_lazy('account:profile')

  def get_object(self):
    return User.objects.get(pk = self.request.user.pk)

  def  get_form_kwargs(self):
    kwargs =  super(Profile, self).get_form_kwargs()
    kwargs.update({
      'user': self.request.user
    })
    return kwargs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['addresses'] = Address.objects.filter(owner=self.request.user)  # آدرس‌های کاربر
    return context  

class Login(LoginView):
  def get_success_url(self):
    user = cast(User, self.request.user)
    if user.is_superuser: #or user.is_colleague:
      return reverse_lazy('account:home')
    else:   
      return reverse_lazy('account:profile')

class PasswordChange(PasswordChangeView):
  success_url = reverse_lazy('account:profile')

class Register(CreateView):
  form_class = SignupForm
  template_name = 'registration/register.html'


  def form_valid(self, form):
    user = form.save(commit=False)
    user.is_active = False  # Deactivate user until activation
    user.save()

    # Generate uid and token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    # Build the activation link
    domain = get_current_site(self.request)
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activation_url = f"http://{domain}{activation_link}"

    # Render the email
    mail_subject = 'فعالسازی حساب کاربری'
    message = render_to_string('registration/activate_account.html', {
        'user': user,
        'activation_url': activation_url,  # Pass the full activation URL
    })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

    return HttpResponse('<h1 style="direction: rtl">لینک فعالسازی به آدرس ایمیل شما ارسال شد.</h1>')
 
def activate(request, uidb64, token):
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()
    return redirect('/login')
  else:
    return HttpResponse('لینک فعالسازی منقضی شده است،  <a href="/register">دوباره امتحان کنید</a>')    

class AddressListView(LoginRequiredMixin ,ListView):
  template_name = 'registration/profile.html'
  model = Address

  def get_queryset(self):
    return Address.objects.filter(user=self.request.user)

class AddressCreateView(LoginRequiredMixin, CreateView):
  model = Address
  form_class = AddressForm
  template_name = 'addresses/address_form.html'
  success_url = reverse_lazy('account:profile')

  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)

class AddressUpdateView(LoginRequiredMixin, UpdateView):
  model = Address
  form_class = AddressForm
  template_name = 'addresses/address_form.html'
  success_url = reverse_lazy('account:profile')

  def form_valid(self, form):
    # تنظیم مالک آدرس به کاربر لاگین شده
    form.instance.owner = self.request.user
    return super().form_valid(form)

class AddressDeleteView(LoginRequiredMixin, DeleteView):
  model = Address
  template_name = 'addresses/address_confirm_delete.html'
  success_url = reverse_lazy('address_list')   

class FamilyMemberListView(LoginRequiredMixin ,ListView):
  template_name = 'registration/profile.html'
  model = FamilyMember
  context_object_name = 'family_members'

  def get_queryset(self):
    return FamilyMember.objects.filter(parent=self.request.user)

class FamilyMemberCreateView(LoginRequiredMixin, CreateView):
  model = FamilyMember
  form_class = FamilyMemberForm
  template_name = 'family/family_form.html'
  success_url = reverse_lazy('account:profile')

  def form_valid(self, form):
    form.instance.parent = self.request.user
    return super().form_valid(form)

class FamilyMemberUpdateView(LoginRequiredMixin, UpdateView):
  model = FamilyMember
  form_class = FamilyMemberForm
  template_name = 'family/family_form.html'
  success_url = reverse_lazy('account:profile')

  def form_valid(self, form):
    # تنظیم مالک آدرس به کاربر لاگین شده
    form.instance.parent = self.request.user
    return super().form_valid(form)

class FamilyMemberDeleteView(LoginRequiredMixin, DeleteView):
  model = FamilyMember
  template_name = 'family/family_confirm_delete.html'
  success_url = reverse_lazy('family_list')  

class PetListView(LoginRequiredMixin ,ListView):
  template_name = 'registration/profile.html'
  model = Pet
  context_object_name = 'pets'

  def get_queryset(self):
    return Pet.objects.filter(owner=self.request.user)

class PetCreateView(LoginRequiredMixin, CreateView):
  model = Pet
  form_class = PetForm
  template_name = 'pets/pet_form.html'
  success_url = reverse_lazy('account:profile')

  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)

class PetUpdateView(LoginRequiredMixin, UpdateView):
  model = Pet
  form_class = PetForm
  template_name = 'pets/pet_form.html'
  success_url = reverse_lazy('account:profile')

  def form_valid(self, form):
    # تنظیم مالک آدرس به کاربر لاگین شده
    form.instance.owner = self.request.user
    return super().form_valid(form)

class PetDeleteView(LoginRequiredMixin, DeleteView):
  model = Pet
  template_name = 'pets/pet_confirm_delete.html'
  success_url = reverse_lazy('account:home')  

class UserListView(LoginRequiredMixin, SuperUserAccessMixin, ListView):
  model = User
  template_name = 'user_management/user_list.html'
  context_object_name = 'users'

class UserCreateView(LoginRequiredMixin, SuperUserAccessMixin, CreateView):
  model = User
  form_class = UserForm
  template_name = 'registration/profile.html'
  success_url = reverse_lazy('user_list')

class UserUpdateView(LoginRequiredMixin, SuperUserAccessMixin, UpdateView):
  model = User
  form_class = UserForm
  template_name = 'registration/profile.html'
  success_url = reverse_lazy('account:user_list')

class UserDeleteView(LoginRequiredMixin, SuperUserAccessMixin, DeleteView):
  model = User
  template_name = 'user_management/user_confirm_delete.html'
  success_url = reverse_lazy('account:user_list')

class NotificationListView(LoginRequiredMixin, ListView):
  model = Notification
  template_name = 'notifications/list.html'
  context_object_name = 'notifications' 

  def get_queryset(self):
    return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    self.mark_as_read()  
    return context

  def mark_as_read(self):
    unread_notifications = Notification.objects.filter(
      recipient = self.request.user, is_read=False
    )
    unread_notifications.update(is_read=True)

class MedicineCreateView(LoginRequiredMixin, CreateView):
    model = Medicine
    fields = ['name', 'description', 'dose', 'useage_way']
    template_name = 'medicine/medicine_form.html'
    success_url = reverse_lazy('account:medicine-create')

    def form_valid(self, form):
      user = self.request.user
      if not user.is_colleague or not user.is_superuser:
          return redirect('account:home')
      form.instance.created_by = user
      return super().form_valid(form)    

class MedicineUpdateView(LoginRequiredMixin, ColleagueRequiredMixin, UpdateView):
    model = Medicine
    fields = ['name', 'description', 'dose', 'useage_way']
    template_name = 'medicine/medicine_form.html'
    success_url = reverse_lazy('account:medicine-create')

    def form_valid(self, form):
      user = self.request.user
      if not user.is_colleague:
          return redirect('account:home')
      form.instance.created_by = user
      return super().form_valid(form)    

class PrescriptionCreateView(LoginRequiredMixin, ColleagueRequiredMixin, CreateView):
    model = Prescription
    fields = ['user', 'medicine', 'interval', 'qty']
    template_name = 'medicine/prescription_form.html'
    success_url = reverse_lazy('account:prescription-create')

    def form_valid(self, form):
        if not self.request.user.is_authenticated or not self.request.user.is_colleague:
            return redirect('account:home')
        form.instance.prescribed_by = self.request.user
        return super().form_valid(form)    

class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'medicine/prescription_list.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Superusers can see all prescriptions with issued_for and issued_by columns
            return Prescription.objects.all()
        elif user.is_colleague:
            # Colleagues can see only the prescriptions they issued
            return Prescription.objects.filter(prescribed_by=user)
        else:
            # Normal users can see only their own prescriptions
            return Prescription.objects.filter(user=user)

class MedicinesListView(LoginRequiredMixin, ListView):
  model = Medicine
  template_name = 'medicine/mediscine_list.html'         
  context_object_name = 'medicines'

  def get_queryset(self):
    user = self.request.user
    if user.is_superuser or user.is_colleague:
      return Medicine.objects.all() 
    else: 
      redirect('account:home')   

class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'medicine/reminder_list.html'
    context_object_name = "reminders"
    
    def get_queryset(self):
        # دریافت یادآوری‌های مربوط به کاربر جاری
        return Reminder.objects.filter(user=self.request.user).order_by('reminder_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # بروزرسانی وضعیت یادآوری‌های مشاهده‌شده
        self.mark_reminders_as_read()
        return context

    def mark_reminders_as_read(self):
        # تغییر وضعیت یادآوری‌های مشاهده‌نشده به "خوانده شده"
        unread_reminders = Reminder.objects.filter(user=self.request.user, is_read=False)
        unread_reminders.update(is_read=True)

def register_device(request):
    if request.method == "POST":
        device_id = request.POST.get("device_id")
        if device_id:
            device, created = GCMDevice.objects.get_or_create(
                user=request.user,
                registration_id=device_id,
                cloud_message_type="FCM",
            )
            device.save()        


@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        subscription = WebPushSubscription.objects.create(
            user=request.user,
            endpoint=data["endpoint"],
            auth_key=data["keys"]["auth"],
            p256dh_key=data["keys"]["p256dh"]
        )
        return JsonResponse({"status": "success"})        