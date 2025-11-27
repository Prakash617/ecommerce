from django.db import models
from django_summernote.widgets import SummernoteWidget
from user_accounts.models import CustomUser
from django.utils.text import slugify


class BlogCategory(models.Model):
    name = models.CharField(max_length=9999)
    url = models.CharField(max_length=9999)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(BlogCategory, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    feature_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    short_content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"


class Comment(models.Model):
    name = models.CharField(max_length=9999, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    comment = models.TextField()
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_on = models.DateField(auto_now_add=True, null=True, blank=True)
    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.name or 'Anonymous'} on {self.post.title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
