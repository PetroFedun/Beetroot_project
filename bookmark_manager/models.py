from django.db import models

class Bookmark(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=200)
    title = models.CharField(max_length=50)

    def get_absolute_url(self):
        return f'/bookmark_manager/'
    
    def __str__(self):
        return self.title
