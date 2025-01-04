from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Medicine, Prescription, Reminder, Notification

# Register your models here.
UserAdmin.fieldsets[2][1]['fields'] = (
  "is_active",
  "is_staff",
  "is_superuser",
  "is_colleague",
  "special_user",
  "groups",
  "user_permissions",
)

UserAdmin.list_display = (
  "username",
  "email", 
  "first_name", 
  "last_name", 
  "is_staff", 
  "is_colleague", 
  "is_special_user",
  "jspecial_user",
  "jcreated_time"
   )
admin.site.register(User, UserAdmin)

admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(Reminder)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'created_at', 'is_read', 'unread_count')

    def unread_count(self, obj):
        return Notification.objects.filter(recipient=obj.recipient, is_read=False).count()
    unread_count.short_description = 'Unread Count'