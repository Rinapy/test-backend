from django.contrib import admin
from .models import CustomUser, Balance, Subscription


class CustomUserAdmin(admin.ModelAdmin):
    """Отображение пользователей в админ панели."""

    list_display = ('email', 'username', 'is_author', 'balance')
    list_filter = ('is_author',)
    search_fields = ('email', 'username')


class BalanceAdmin(admin.ModelAdmin):
    """Отображение балансов в админ панели."""

    list_display = ('amount',)
    list_filter = ('amount',)


class SubscriptionAdmin(admin.ModelAdmin):
    """Отображение подписок в админ панели."""
    
    list_display = ('user', 'course')
    list_filter = ('user', 'course')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
