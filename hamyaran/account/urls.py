from django.urls import path
from .views import ServiceList, ServiceCreate, category, ServiceUpdate, ServiceDelete, Profile, AddressCreateView, AddressUpdateView, AddressDeleteView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, NotificationListView, MedicineCreateView, PrescriptionCreateView, ReminderListView, PrescriptionListView, PetListView, PetCreateView, PetUpdateView, PetDeleteView, FamilyMemberListView, FamilyMemberCreateView, FamilyMemberUpdateView, FamilyMemberDeleteView, MedicinesListView, MedicineUpdateView

app_name = 'account'

urlpatterns = [
  path('services/', ServiceList.as_view(), name="home"),
  path('users/', UserListView.as_view(), name='user-list'),
  path('users/add/', UserCreateView.as_view(), name='user-add'),
  path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user-edit'),
  path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
  path('service/create', ServiceCreate.as_view(), name='service-create'),
  path('service/update/<int:pk>', ServiceUpdate.as_view(), name='service-update'),
  path('service/delete/<int:pk>', ServiceDelete.as_view(), name='service-delete'),
  path('profile/', Profile.as_view(), name='profile'),
  path('services/<slug:slug>', category, name='category'),
  path('addresses/create/', AddressCreateView.as_view(), name='address_create'),
  path('addresses/<int:pk>/update/', AddressUpdateView.as_view(), name='address_update'),
  path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),
  path('family/create/', FamilyMemberCreateView.as_view(), name='family_create'),
  path('family/<int:pk>/update/', FamilyMemberUpdateView.as_view(), name='family_update'),
  path('family/<int:pk>/delete/', FamilyMemberDeleteView.as_view(), name='family_delete'),
  path('pets/create/', PetCreateView.as_view(), name='pet_create'),
  path('pets/<int:pk>/update/', PetUpdateView.as_view(), name='pet_update'),
  path('pets/<int:pk>/delete/', PetDeleteView.as_view(), name='pet_delete'),
  path('notifications/', NotificationListView.as_view(), name='notifications'),
  path('medicine/create/', MedicineCreateView.as_view(), name='medicine-create'),
  path('medicine/<int:pk>/update/', MedicineUpdateView.as_view(), name='medicine-update'),
  path('medicines/', MedicinesListView.as_view(), name='medicine-list'),
  path('prescription/create/', PrescriptionCreateView.as_view(), name='prescription-create'),
  path('prescriptions/', PrescriptionListView.as_view(), name='prescription-list'),
  path('reminders/', ReminderListView.as_view(), name='reminder-list'),
]
