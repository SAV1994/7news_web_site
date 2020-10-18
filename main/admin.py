from django.contrib import admin
from .models import User, Rule


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'date_joined', 'is_active']
    model = User


class RulesAdmin(admin.ModelAdmin):
    model = Rule


admin.site.register(Rule, RulesAdmin)
admin.site.register(User, UserAdmin)