from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from . models import Meal
import os

class MealAdmin(admin.ModelAdmin):
    def file(self):
        class Meta:
            allow_tags = True
            verbose_name = _('File')

        return format_html(u'<a href="{0}">{1}</a>',
                           self.get_absolute_url(),
                           os.path.basename(self.file.name))

    list_display = ('id', file, 'expiration_time')
    ordering = ('expiration_time',)
    fields = ('id', 'file', 'expiration_time')

admin.site.register(Meal, MealAdmin)
