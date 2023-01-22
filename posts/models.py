from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    uploader = models.CharField(blank=True, null=True, max_length=200)
    description = models.TextField(blank=True, null=True, max_length=400)
    likes = models.ManyToManyField(User, related_name='posts', blank=True)


    @property
    def total_likes(self):
        return self.likes.all().count()

    def __str__(self):
        return self.uploader

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField(max_length=400)
    date_added = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return '%s' % (self.name)
