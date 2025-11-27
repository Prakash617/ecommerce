from django.contrib import admin
from .models import NewsletterEmail
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
class NewsletterEmailAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(NewsletterEmail,NewsletterEmailAdmin)