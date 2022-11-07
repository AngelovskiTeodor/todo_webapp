from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from todo_webapp.models import TodoCard, TodoItem
from todo_webapp.serializers import TodoCardCreateSerializer, TodoCardDetailsSerializer, TodoItemCreateSerializer, TodoItemDetailsSerializer


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def cards_list(request):
    if request.method != "GET":
        print("Request method for cards_list is not GET")
        pass
    todo_cards = TodoCard.objects.all()
    cards_serializer = TodoCardDetailsSerializer(todo_cards, many=True, context={'request': request})
    return JsonResponse(cards_serializer.data, safe=False)


@api_view(['POST', 'PUT'])
@csrf_exempt
@permission_classes([AllowAny])
def card_create(request):
    if request.method in ["POST", "PUT"]:
        new_card_data = request.data    #   JSONParser().parse(request)     # Parse request first???
        print("new_card_data: {}".format(new_card_data))    # debugging
        #new_card_data['user'] = request.user    # ne e vozmozno bidejki request.data e konstanta (immutable)
        #print("new_card_data (after added user): {}".format(new_card_data))    # debugging
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
        return HttpResponse(status=404)
    if request.method == "GET":
        card_serializer = TodoCardDetailsSerializer(card, context={'request': request})
        return JsonResponse(card_serializer.data)
    elif request.method == "PUT":
        new_card_data = request.data    #   JSONParser().parse(request)     # Parse request???
        card_serializer = TodoCardDetailsSerializer(card, data=new_card_data)
        if card_serializer.is_valid():
            card_serializer.save()
            return JsonResponse(card_serializer.data, status=201)
        return JsonResponse(card_serializer.errors, status=400)
    elif request.method == "DELETE":
        card.delete()
        return HttpResponse(status=204)
    else:
        print("Request Method "+request.method+" not supported for this route")


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@permission_classes([AllowAny])
def item_details(request, item_id):
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
    try:
        item = TodoItem.objects.get(pk=item_id)
    except TodoItem.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        item_serializer = TodoItemDetailsSerializer(item)
        return JsonResponse(item_serializer.data)
    elif request.method == "PUT":
        new_item_data = request.data #   JSONParser().parse(request)     # Parse request first???
        item_serializer = TodoItemCreateSerializer(item, data=new_item_data, partial=True)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data)
        return JsonResponse(item_serializer.errors, status=400)
    elif request.method == "DELETE":
        item.delete()
        return HttpResponse(status=204)
    else:
        print("Request Method "+request.method+" not supported for this route")
    pass


@api_view(['POST', 'PUT'])
@csrf_exempt
@permission_classes([AllowAny])
def item_create(request, card_id):
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
    if request.method not in ["POST", "PUT"]:
        print("Request method for item_details is not POST or PUT")
        pass
    new_item_data = request.data    #   JSONParser().parse(request)     # Parse request first
    item_serializer = TodoItemCreateSerializer(data=new_item_data)
    card = TodoCard.objects.get(id=card_id) # na save funkcijata treba da se predade TodoCard objekt/instanca namesto card_id
    if item_serializer.is_valid():
        item_serializer.save(card_id=card)
        return JsonResponse(item_serializer.data, status=201)
    return JsonResponse(item_serializer.errors, status=400)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def card_items(request, card_id):
    #print(request.__dict__)      # debugging
    #print(request.data.__dict__)      # debugging
    if request.method != "GET":
        print("Request method for card_items is not GET")
        pass
    try:
        card = TodoCard.objects.get(pk=card_id)
        print(card)     # debugging
    except TodoCard.DoesNotExist:
        return HttpResponse(status=404)
    items = TodoItem.objects.filter(card_id=card_id)
    items_serializer = TodoItemDetailsSerializer(items, many=True)
    return JsonResponse(items_serializer.data, safe=False)

