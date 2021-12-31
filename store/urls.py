from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.all_products, name="list"),
    path('item/<slug:slug>/', views.product_detail, name="product_detail"),
    path('category/<slug:slug>/', views.category_detail, name="category_detail"),

]

