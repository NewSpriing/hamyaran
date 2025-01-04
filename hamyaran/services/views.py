from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Service, Category, Order
from django.core.paginator import Paginator
from account.models import User
from django.views.generic.edit import FormView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from account.forms import OrderForm

# Create your views here.
def home(request):
  return render(request, 'services/index.html')

def services(request):
  available_services = Service.objects.accessible()
  paginator = Paginator(available_services, 5)
  page = request.GET.get('page')
  servicesList = paginator.get_page(page)
  context = { 
  'services': servicesList,
}
  return render(request, 'services/services.html', context)

class ServiceList(ListView):
  queryset =  Service.cats.available()
  template_name = 'services/services.html'
  paginate_by = 5

def category(request, slug):
  category = get_object_or_404(Category, slug=slug, 
  status=True)
  available_services = Service.cats.available()
  paginator = Paginator(available_services, 5)
  page = request.GET.get('page')
  servicesList = paginator.get_page(page)
  context = { 
    'category' : category, 
    'services': servicesList,
}
  return render(request, 'services/category.html', context)

class CategoryList(ListView):
  paginate_by = 5
  template_name = 'services/category.html'

  def get_queryset(self):
    global category
    slug = self.kwargs.get('slug')
    category = get_object_or_404(Category.objects.accessible(), slug=slug)
    return category.services.available()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["category"] = category
    return context

class SearchList(ListView):
  paginate_by = 5
  template_name = 'services/search.html'

  def get_queryset(self):
    search = self.request.GET.get('q')
    return Service.objects.filter(name__icontains=search)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["search"] = self.request.GET.get('q')
    return context
      
class OrderView(CreateView):
  model = Order
  form_class = OrderForm
  template_name = "services/order_form.html"


  def get_form_kwargs(self):
    kwargs =  super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def form_valid(self, form):
    form.instance.user = self.request.user
    self.object = form.save()
    return super().form_valid(form)  

  def get_success_url(self):
    return reverse('services:order-success', kwargs={'pk': self.object.pk})

class OrderSuccess(LoginRequiredMixin, DeleteView):
  model = Order
  template_name = 'services/order_success.html'    
  context_object_name = 'order'
       
def Pricing(request):
  return render(request, 'pricing/pricing.html')           