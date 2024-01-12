from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=5000)
    description = models.TextField(max_length=5000, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    reminder = models.DateTimeField()
    due = models.DateTimeField()
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']