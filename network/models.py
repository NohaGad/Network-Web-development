from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F


class User(AbstractUser):
    pass 

class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id','following_user_id'], 
                 name="unique_followers"),
            models.CheckConstraint(
                name="User can't follow itself",
                check=~models.Q(user_id=models.F("following_user_id")))
        ]
        ordering = ["-created"]
    @property
    def count_following(self):
        return self.user_id.count()
    
    @property
    def count_followers(self):
        return self.following_user_id.count()

class Post(models.Model):
    post_text = models.TextField(max_length=1024)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    likers = models.ManyToManyField(User, blank=True, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def total_likes (self):
        return self.likes.count()
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.owner.username,
            "post_text": self.post_text,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "updated_at": self.updated_at.strftime("%b %d %Y, %I:%M %p"),
        }

    class Meta:
        ordering = ['-created_at']
    