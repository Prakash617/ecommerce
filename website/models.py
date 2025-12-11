from django.db import models

# Create your models here.

class Carousal(models.Model):
    title = models.CharField("Title", max_length=9999, null=True, blank=True)
    link = models.URLField("Link", null=True, blank=True)
    image = models.ImageField("Carousel Image", upload_to='carousel_images/')
    link_text = models.CharField("Link Text", max_length=999999, null=True, blank=True)

    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = "Carousels"

    def __str__(self):
        return self.title


class FaqsTopic(models.Model):
    title = models.CharField("Topic Title", max_length=99999)

    class Meta:
        verbose_name = "FAQ Topic"
        verbose_name_plural = "FAQ Topics"

    def __str__(self):
        return self.title


class Faqs(models.Model):
    topic = models.ForeignKey(FaqsTopic, verbose_name="Topic", on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField("Question", max_length=99999)
    answer = models.TextField("Answer")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Menus(models.Model):
    name = models.CharField("Menu Name", max_length=9999)
    url = models.CharField("URL", max_length=9999)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.name


class Careers(models.Model):
    title = models.CharField("Job Title", max_length=9999)
    created_at = models.DateField("Created At", auto_now_add=True)
    description = models.TextField("Description", null=True, blank=True)
    expire_at = models.DateTimeField("Expires At", null=True, blank=True)
    image = models.ImageField("Career Image", upload_to='careers_images/')
    quantity = models.IntegerField("Quantity")

    class Meta:
        verbose_name = "Career"
        verbose_name_plural = "Careers"

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    email = models.EmailField("Subscriber Email")
    subscribed_at = models.DateTimeField("Subscribed At", auto_now_add=True)
    opt_out = models.BooleanField("Opted Out", default=False)

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

    def __str__(self):
        return self.email


class TermsAndCondition(models.Model):
    name = models.CharField("Title", max_length=99999, null=True, blank=True)
    html_content = models.TextField("Terms and Conditions Content")

    class Meta:
        verbose_name = "Terms and Condition"
        verbose_name_plural = "Terms and Conditions"

    def __str__(self):
        return self.name


class PrivacyPolicy(models.Model):
    name = models.CharField("Title", max_length=99999, null=True, blank=True)
    html_content = models.TextField("Privacy Policy Content")

    class Meta:
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"

    def __str__(self):
        return self.name
    
from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=200,)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']
