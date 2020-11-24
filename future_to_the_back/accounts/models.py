from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')
    profile_image = ProcessedImageField(
        upload_to='%Y/%m/%d/',
        blank=True, 
        format='JPEG',
        processors=[Thumbnail(300, 200)],
        options={'quility' : 90}
    )

    def __str__(self):
        return self.username