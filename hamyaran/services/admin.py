from django.contrib import admin
from .models import Service, Category

#actions
def make_available(modeleadmin, request, queryset):
  rows_updated = queryset.update(status=True)
  if rows_updated == 1:
    message_bit = "مورد دردسترس قرار گرفت"
  else:
    message_bit = "مورد دردسترس قرار گرفتند"
  modeleadmin.message_user(request, '{} {}'.format(rows_updated, message_bit))
make_available.short_description = 'نمایش بده'

def make_unavailable(modeleadmin, request, queryset):
  rows_updated = queryset.update(status=False)
  if rows_updated == 1:
    message_bit = "مورد از دسترس خارج شد"
  else:
    message_bit = "مورد از دسترس خارج شدند"
  modeleadmin.message_user(request, '{} {}'.format(rows_updated, message_bit))
make_unavailable.short_description = 'نمایش نده'


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('position', 'title', 'slug', 'status')
  list_filter = (['title'])
  search_fields = (['status', 'title'])
  ordering = ('status', 'position')
  actions = [make_available, make_unavailable]


admin.site.register(Category, CategoryAdmin)

class ServiceAdmin(admin.ModelAdmin):
  list_display = ('name', 'category', 'cost', 'therapist', 'status')
  list_filter = ['category', 'status']
  search_fields = ['name','cost','therapist']
  ordering = ['category']
  actions = [make_available, make_unavailable]
"""   prepopulated_fields ={'therapist':['cost*80%']} """


admin.site.register(Service, ServiceAdmin)