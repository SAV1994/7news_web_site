from django.contrib import admin
from .models import User, Rule, News, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'date_joined', 'is_active']
    model = User


class CommentInLine(admin.TabularInline):
    model = Comment


class RulesAdmin(admin.ModelAdmin):
    model = Rule


class NewsAdmin(admin.ModelAdmin):
    model = News
    inlines = (CommentInLine,)


class CommentAdmin(admin.ModelAdmin):
    model = Comment


admin.site.register(Rule, RulesAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
