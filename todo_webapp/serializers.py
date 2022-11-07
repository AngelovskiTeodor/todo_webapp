from rest_framework import serializers
from todo_webapp.models import TodoCard, TodoItem

# Django REST Framework Docs Reference:
# https://www.django-rest-framework.org/api-guide/relations/

class TodoCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCard
        fields = ['id', 'title', 'description', 'deadline']

class TodoCardDetailsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    #items = serializers.PrimaryKeyRelatedField(many=True, queryset=TodoItem.objects.all())  # frla exception bidejki vo models.py nema items field vo klasata TodoCard
    items = serializers.SlugRelatedField(many=True, slug_field='id', read_only=True, allow_null=True)  # BUG: does not display the items property in JSON at all
    #items = TodoItemDetailsSerializer(many=True)
    
    class Meta:
        model = TodoCard
        fields = [ 'id', 'title', 'user', 'description', 'deadline', 'items']    # da se vnimava na 'items' bidejki vo models.py nema items pole vo ToDoCard, tuku povrzuvanjeto e izvrseno preku ToDoItem
        depth = 1

class TodoItemDetailsSerializer(serializers.ModelSerializer):
    card_id = serializers.PrimaryKeyRelatedField(queryset=TodoCard.objects.all())

    class Meta:
        model = TodoItem
        fields = [ 'id', 'task', 'is_completed', 'card_id' ]

class TodoItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id', 'task', 'is_completed']
