from django.contrib import admin

from .models import Course, Group

class CourseAdmin(admin.ModelAdmin):
    """Отображение курсов в админ панели."""

    list_display = ('title', 'author', 'start_date', 'get_subscribers', 'price')
    list_filter = ('author', 'price', 'start_date')
    list_editable = ('author', 'start_date', 'price')

class GroupAdmin(admin.ModelAdmin):
    """Отображение групп в админ панели."""
    list_display = ('course', 'get_subscribers')
    list_filter = ('course',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Group, GroupAdmin)
