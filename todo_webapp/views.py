#from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from todo_webapp.models import TodoCard, TodoItem
from todo_webapp.serializers import TodoCardSerializer, TodoItemSerializer

@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def cards_list(request):
    #print(request)      # debugging
    #print(request.data)      # debugging
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
    if request.method != "GET":
        # error handling
        print("Request method for cards_list is not GET")
        pass
    todo_cards = TodoCard.objects.all()
    cards_serializer = TodoCardSerializer(todo_cards, many=True)
    return JsonResponse(cards_serializer.data, safe=False)

@api_view(['POST', 'PUT'])
@csrf_exempt
@permission_classes([AllowAny])
#@authentication_classes([TokenAuthentication])
def card_create(request):
    #print(request)      # debugging
    #print(request.data)      # debugging
    #print(request.__dict__)      # debugging
    print('Request Headers: '.format(request.META))     # debugging
    print('Request Authorization: '.format(request.auth))       # debugging
    print('Request to create new card by user {0}'.format(request.user))     # debugging
    if request.method in ["POST", "PUT"]:
        new_card_data = request.data    #   JSONParser().parse(request)     # Parse request first???
        #if request.user is None:
            #new_card_data['user'] = request.user    # the user must be logged in
        #else:
            #new_card_data['user'] = 'admin'     # debugging
            #print('The user is not authorized')
            #raise Exception('The user is not authorized')
        card_serializer = TodoCardSerializer(data=new_card_data)
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
def card_details(request, card_pk):
    #print(request)      # debugging
    #print(request.data)      # debugging
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
    try:
        card = TodoCard.objects.get(pk=card_pk)
    except TodoCard.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        card_serializer = TodoCardSerializer(card)
        return JsonResponse(card_serializer.data)
    elif request.method == "PUT":
        new_card_data = request.data    #   JSONParser().parse(request)     # Parse request???
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

@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@permission_classes([AllowAny])
def item_details(request, item_pk):
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
    try:
        item = TodoItem.objects.get(pk=item_pk)
    except TodoItem.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        item_serializer = TodoItemSerializer(item)
        return JsonResponse(item_serializer.data)
    elif request.method == "PUT":
        new_item_data = request.data #   JSONParser().parse(request)     # Parse request first???
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

@api_view(['POST', 'PUT'])
@csrf_exempt
@permission_classes([AllowAny])
def item_create(request):
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
    if request.method not in ["POST", "PUT"]:
        # error handling
        print("Request method for item_details is not POST or PUT")
        pass
    new_item_data = request.data    #   JSONParser().parse(request)     # Parse request first
    item_serializer = TodoItemSerializer(data=new_item_data)
    if item_serializer.is_valid():
        item_serializer.save()
        return JsonResponse(item_serializer.data, status=201)
    return JsonResponse(item_serializer.errors, status=400)

@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def card_items(request, card_pk):
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
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

