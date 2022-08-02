#from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from todo_webapp.models import TodoCard, TodoItem
from todo_webapp.serializers import TodoCardSerializer, TodoItemSerializer

@csrf_exempt
def cards_list(request):
    if request.method != "GET":
        # error handling
        print("Request method for cards_list is not GET")
        pass
    todo_cards = TodoCard.objects.all()
    cards_serializer = TodoCardSerializer(todo_cards, many=True)
    return JsonResponse(cards_serializer.data, safe=False)

@csrf_exempt
def card_create(request):
    if request.method in ["POST", "PUT"]:
        new_card_data = JSONParser().parse(request)
        card_serializer = TodoCardSerializer(data=new_card_data)
        if card_serializer.is_valid():
            card_serializer.save()
            return JsonResponse(card_serializer.data, status=201)
        return JsonResponse(card_serializer.errors, status=400)
    else:
        print("Request method for card_create is not POST or PUT")

@csrf_exempt
def card_details(request, card_pk):
    try:
        card = TodoCard.objects.get(pk=card_pk)
    except TodoCard.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        card_serializer = TodoCardSerializer(card)
        return JsonResponse(card_serializer.data)
    elif request.method == "PUT":
        new_card_data = JSONParser().parse(request)
        card_serializer = TodoCardSerializer(card, data=new_card_data)
        if card_serializer.is_valid():
            card_serializer.save()
            return JsonResponse(card_serializer.data, status=201)
        return JsonResponse(card_serializer.errors, status=400)
    elif request.method == "DELETE":
        card.delete()
        return HttpResponse(status=204)
    else:
        # error handling: unsuported request method
        print("Request Method "+request.method+" not supported for this route")

@csrf_exempt
def item_details(request, item_pk):
    try:
        item = TodoItem.objects.get(pk=item_pk)
    except TodoItem.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        item_serializer = TodoItemSerializer(item)
        return JsonResponse(item_serializer.data)
    elif request.method == "PUT":
        new_item_data = JSONParser().parse(request)
        item_serializer = TodoItemSerializer(item, data=new_item_data)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data)
        return JsonResponse(item_serializer.errors, status=400)
    elif request.method == "DELETE":
        item.delete()
        return HttpResponse(status=204)
    else:
        # error handling: unsuported request method
        print("Request Method "+request.method+" not supported for this route")
    pass

@csrf_exempt
def item_create(request):
    if request.method not in ["POST", "PUT"]:
        # error handling
        print("Request method for item_details is not POST or PUT")
        pass
    new_item_data = JSONParser().parse(request)
    item_serializer = TodoItemSerializer(data=new_item_data)
    if item_serializer.is_valid():
        item_serializer.save()
        return JsonResponse(item_serializer.data, status=201)
    return JsonResponse(item_serializer.errors, status=400)

@csrf_exempt
def card_items(request, card_pk):
    if request.method != "GET":
        # error handling
        print("Request method for card_items is not GET")
        pass
    try:
        TodoCard.objects.get(pk=card_pk)
    except TodoCard.DoesNotExist:
        return HttpResponse(status=404)
    items = TodoItem.objects.filter(lambda item: item.card==card_pk).values()
    items_serializer = TodoItemSerializer(items, many=True)
    return JsonResponse(items_serializer.data, safe=False)

