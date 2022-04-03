from django.urls import path
from . import views

urlpatterns = [
    path('create', views.CreateToken, name='create'),
    path('list', views.ListTokens, name='list'),
    path('total_supply', views.TokenTotalSupply, name='total_supply')
]