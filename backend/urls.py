"""
URL configuration for backend project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_image, name='predict_image'),
    path('items/', views.get_items_all, name="get all items"),
    path('item', views.get_item_by_id, name="get item by item id"),
    path('item/date', views.get_items_by_date, name="get item by date add"),
    path('item/name', views.get_items_by_name, name="get item by item name"),
    path('item/create', view=views.create_new_item, name="create new item")
]