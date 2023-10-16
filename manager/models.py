from django.db import models
from django.contrib.auth.models import User 

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    url = models.URLField()
    description = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    tags = models.ManyToManyField('Tag', blank=True, related_name='bookmarks')

    def get_absolute_url(self):
        return f'/manager/'
    
    def __str__(self):
        return self.title

class Tag(models.Model): 
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
