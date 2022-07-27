from rest_framework import serizalizers
from models import TodoCard, TodoItem

class TodoCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoCard
        fields = [ 'title', 'description', 'items', 'deadline' ]

class TodoItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoItem
        fields = [ 'task', 'is_completed', 'card' ]