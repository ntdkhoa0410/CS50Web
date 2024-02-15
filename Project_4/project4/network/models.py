from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField(blank=False)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", related_name="liked_posts", blank=True)

    def serialize(self):
        likes_count = self.likers.count()  #
        likers = [user.id for user in self.likers.all()]
        
        return {
            "id": self.id,
            "content": self.content,
            "author": self.author.username,
            "author_id": self.author.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": likes_count,
            "likers" : likers,
        }

class Following_System(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    following = models.ManyToManyField("User", related_name="following")

    def __str__(self):
        return f"User {self.user} is following {', '.join([user.username for user in self.following.all()])}"
