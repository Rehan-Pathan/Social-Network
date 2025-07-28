from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)

    def serialize_profile(self, current_user):
        return {
            "username": self.username,
            "followers_count": self.followers.count(),
            "following_count": self.following.count(),
            "is_following": current_user.is_authenticated and self in current_user.following.all(),
            "is_own_profile": current_user == self
        }

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
    
    def serialize(self, current_user=None):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": localtime(self.timestamp).strftime("%b %d %Y, %I:%M %p"),
            "likes_count": self.like_count(),
            "liked_by_current_user": current_user.is_authenticated and self.likes.filter(id=current_user.id).exists() if current_user else False
        }