from django.contrib import admin
from .models import CustomUser, Balance, Subscription, Course


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_author')
    list_filter = ('is_author',)
    search_fields = ('email', 'username')


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('amount',)
    list_filter = ('amount',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_filter = ('user', 'course')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Course, CourseAdmin)
