from django.db import models
from django.conf import settings
from django.utils.text import slugify

def blog_image_path(instance, filename):
    # Create unique path: blogs/user_id/filename
    return f'blogs/{instance.author.id}/{filename}'

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.URLField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
