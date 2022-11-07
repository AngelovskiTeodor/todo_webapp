from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from todo_webapp.models import TodoCard, TodoItem
from todo_webapp.serializers import TodoCardCreateSerializer, TodoCardDetailsSerializer, TodoItemCreateSerializer, TodoItemDetailsSerializer


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def cards_list(request):
    todo_cards = TodoCard.objects.all()
    cards_serializer = TodoCardDetailsSerializer(todo_cards, many=True, context={'request': request})
    return JsonResponse(cards_serializer.data, safe=False)


@api_view(['POST', 'PUT'])
@csrf_exempt
@permission_classes([AllowAny])
def card_create(request):
    if request.method in ["POST", "PUT"]:
        new_card_data = request.data
        card_serializer = TodoCardCreateSerializer(data=new_card_data, context={'request': request})
        if card_serializer.is_valid():
            card_serializer.save(user=request.user)
            return JsonResponse(card_serializer.data, status=201)
        return JsonResponse(card_serializer.errors, status=400)
    else:
        print("Request method for card_create is not POST or PUT")
        raise Exception("Request method for card_create is not POST or PUT")


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
@csrf_exempt
def card_details(request, card_id):
    try:
        card = TodoCard.objects.get(pk=card_id)
    except TodoCard.DoesNotExist:
        return JsonResponse({'message': 'Invalid ID'}, status=404)
    if request.method == "GET":
        card_serializer = TodoCardDetailsSerializer(card, context={'request': request})
        return JsonResponse(card_serializer.data)
    elif request.method == "PUT":
        new_card_data = request.data
        card_serializer = TodoCardDetailsSerializer(card, data=new_card_data)
        if card_serializer.is_valid():
            card_serializer.save()
            return JsonResponse(card_serializer.data, status=201)
        return JsonResponse(card_serializer.errors, status=400)
    elif request.method == "DELETE":
        card.delete()
        return JsonResponse({'message': 'ToDo Card Deleted Successfully.'}, status=204)
    else:
        print("Request Method "+request.method+" not supported")
        return JsonResponse({'message': "Request Method "+request.method+" not supported"}, status=404)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@permission_classes([AllowAny])
def item_details(request, item_id):
    try:
        item = TodoItem.objects.get(pk=item_id)
    except TodoItem.DoesNotExist:
        return JsonResponse({'message': 'Invalid ID.'}, status=404)
    if request.method == "GET":
        item_serializer = TodoItemDetailsSerializer(item)
        return JsonResponse(item_serializer.data)
    elif request.method == "PUT":
        new_item_data = request.data
        item_serializer = TodoItemCreateSerializer(item, data=new_item_data, partial=True)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data)
        return JsonResponse(item_serializer.errors, status=400)
    elif request.method == "DELETE":
        item.delete()
        return JsonResponse({'message': 'ToDo Item Deleted Successfully.'}, status=204)
    else:
        print("Request Method "+request.method+" not supported for this route")
        return JsonResponse({'message': "Request Method "+request.method+" not supported"}, status=404)


@api_view(['POST', 'PUT'])
@csrf_exempt
@permission_classes([AllowAny])
def item_create(request, card_id):
    new_item_data = request.data
    item_serializer = TodoItemCreateSerializer(data=new_item_data)
    card = TodoCard.objects.get(id=card_id) # .save() method requires ToDoCard object/instance instead of just card_id
    if item_serializer.is_valid():
        item_serializer.save(card_id=card)
        return JsonResponse(item_serializer.data, status=201)
    return JsonResponse(item_serializer.errors, status=400)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def card_items(request, card_id):
    try:
        card = TodoCard.objects.get(pk=card_id)
    except TodoCard.DoesNotExist:
        return JsonResponse({'message': 'Invalid ID.'}, status=404)
    items = TodoItem.objects.filter(card_id=card_id)
    items_serializer = TodoItemDetailsSerializer(items, many=True)
    return JsonResponse(items_serializer.data, safe=False)

