from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    header = models.CharField(max_length=50)
    text = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.post


