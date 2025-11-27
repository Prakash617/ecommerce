from django.db import models

class NewsletterEmail(models.Model):
    topic = models.CharField("Topic", max_length=9999)
    content = models.TextField("Email Content")

    class Meta:
        verbose_name = "Newsletter Email"
        verbose_name_plural = "Newsletter Emails"

    def __str__(self):
        return self.topic
