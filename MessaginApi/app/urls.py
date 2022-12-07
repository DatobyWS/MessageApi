from django.urls import path,include
from app.views import MessageAll
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('',MessageAll,basename='messages')


urlpatterns = [
    path('messages/',include(router.urls)),
    path('unread/', MessageAll.as_view({'get':'unread'}),name='unread'),
]

