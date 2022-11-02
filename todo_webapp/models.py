from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoCard(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField()
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)

class TodoItem(models.Model):
    card = models.ForeignKey(TodoCard, on_delete=models.CASCADE, blank=False, null=False)
    task = models.CharField(max_length=512)
    is_completed = models.BooleanField(default=None)