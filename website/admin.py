from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Carousal)
admin.site.register(Careers)
admin.site.register(Faqs)
admin.site.register(FaqsTopic)
admin.site.register(Menus)

from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
class TermsAndConditionAdmin(SummernoteModelAdmin):
    summernote_fields = ('html_content',)

admin.site.register(TermsAndCondition, TermsAndConditionAdmin)


class PrivacyPolicyAdmin(SummernoteModelAdmin):
    summernote_fields = ('html_content',)

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)