from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.urls import reverse_lazy
from django.http import Http404
from services.models import Service
from .models import User, FamilyMember, Address, Pet

class FieldsMixin():
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_superuser:
      self.fields = ['name', 'category', 'cost', 'therapist']
    else:
      raise reverse_lazy('account:home')
    return super().dispatch(request, *args, **kwargs)


class EditAccessMixin():
  def dispatch(self, request, pk, *args, **kwargs):
    service = get_object_or_404(Service, pk=pk)
    if request.user.is_superuser:
      return super().dispatch(request, *args, **kwargs)
    else:
      raise reverse_lazy('account:home')


class SuperUserAccessMixin():
  def dispatch(self, request, *args, **kwargs):  
    if request.user.is_superuser:
      return super().dispatch(request, *args, **kwargs)
    else:
      raise reverse_lazy('account:home')


class ColleagueRequiredMixin():
    """Mixin to check if the user has is_colleague=True"""

    def dispatch(self, request, *args, **kwargs):
        # بررسی اینکه آیا کاربر وارد شده است و دسترسی دارد
        if not request.user.is_colleague or not request.user.is_superuser:
            return redirect('account:home')  # به یک ویو یا URL خاص ریدایرکت می‌شود
        return super().dispatch(request, *args, **kwargs)

class UserContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(owner=self.request.user)
        context['family_members'] = FamilyMember.objects.filter(parent=self.request.user)
        context['pets'] = Pet.objects.filter(owner=self.request.user)
        return context