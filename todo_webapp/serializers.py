from rest_framework import serializers
from todo_webapp.models import TodoCard, TodoItem

class TodoCardSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = TodoCard
        fields = [ 'title', 'description', 'deadline' ]   # [ 'title', 'user', 'description', 'items', 'deadline' ]

class TodoItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoItem
        fields = [ 'task', 'is_completed', 'card' ]