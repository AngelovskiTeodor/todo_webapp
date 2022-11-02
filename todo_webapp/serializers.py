from rest_framework import serializers
from todo_webapp.models import TodoCard, TodoItem

class TodoCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoCard
        fields = [ 'title', 'description', 'deadline' ]

class TodoItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoItem
        fields = [ 'task', 'is_completed', 'card' ]