from django.contrib import admin
from . import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'datetime_create',)


admin.site.register(models.Book)

admin.site.register(models.Comment, CommentAdmin)

