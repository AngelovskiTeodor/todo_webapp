from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoCard(models.Model):
    """
    Django Model for Card with ToDo Items/Tasks.
    Has the folowing properties:
    - id
    - title
    - user
    - description
    - deadline
    """
    # Auto generated primery key id, type BigInt
    title = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)    # blank se odnesuva dali pri validacija moze da bide prazno ova pole, a null se odnesuva dali vo databaza moze da bide prazno ova pole
    description = models.TextField()
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)

class TodoItem(models.Model):
    """
    Django Model for ToDo Item/Task
    Has the folowoing properties:
    - id
    - card_id
    - task
    - is_completed
    """
    # Auto generated primary key id, type BigInt
    card_id = models.ForeignKey(TodoCard, on_delete=models.CASCADE, blank=True, null=False)
    task = models.CharField(max_length=512)
    is_completed = models.BooleanField(default=None)
