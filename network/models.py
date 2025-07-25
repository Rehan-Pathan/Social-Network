from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    
    def like_count(self):
        return self.likes.count()


    def __str__(self):
        local_timestamp = localtime(self.timestamp)
        return f"{self.user} posted at {local_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}"