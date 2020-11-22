from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


# Create your models here.
class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='reviews'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_articles'
    )
    title = models.CharField(max_length=50)
    photo = ProcessedImageField(
        upload_to='%Y/%m/%d/',
        blank=True, 
        format='JPEG',
        processors=[Thumbnail(300, 200)],
        options={'quility' : 90}
    )
    rate = models.FloatField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.title}'



class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
