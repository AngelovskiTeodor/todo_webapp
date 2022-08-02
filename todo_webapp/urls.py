from django.urls import path
from todo_webapp import views

urlpatterns = [
    path("cards/", views.cards_list, name="cards_list"),
    path("card", views.card_create, name="card_create"),
    path("card/<int:card_pk>/", views.card_details, name="card_details"),
    path("item", views.item_create, name="item_create"),
    path("item/<int:item_pk>/", views.item_details, name="item_details"),
    path("card/<int:card_pk>/items", views.card_items, name="card_items"),
]