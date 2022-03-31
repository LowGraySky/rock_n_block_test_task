from django.urls import  path
import views

urlpatterns = [
    path('tokens/create', views.CreateToken, name='create'),
    path('tokens/list', views.ListTokens, name='list'),
    path('tokens/total_supply', views.TokenTotalSupply, name='total_supply')
]