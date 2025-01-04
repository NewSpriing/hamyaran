from django.urls import path
from .views import home, ServiceList, category, services, CategoryList, OrderView, OrderSuccess, SearchList, Pricing


app_name = 'services'
urlpatterns = [
  path('', home, name='home'),
  path('pricing/', Pricing, name='pricing'),
  path('services/', ServiceList.as_view(), name='services'),
  path('services/<slug:slug>', CategoryList.as_view(), name='category'),
  path('search/', SearchList.as_view(), name='search'),
  path('search/<slug:slug>', SearchList.as_view(), name='search'),
  path('order/', OrderView.as_view(), name='order'),
  path('order-success/<int:pk>', OrderSuccess.as_view(), name='order-success'),
]
