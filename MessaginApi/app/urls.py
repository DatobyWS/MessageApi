from django.urls import path
from app.views import MessageAll,MessageOne,MessageNotRead
from rest_framework.request import Request
from rest_framework.authtoken import views

urlpatterns = [
    path('messages/',MessageAll.as_view(),name=''),
    path('api-token-auth/', views.obtain_auth_token),
    path('messages/<str:pk>',MessageOne.as_view(),name=''),
    path('messages/unread/',MessageNotRead.as_view(),name='')
]
