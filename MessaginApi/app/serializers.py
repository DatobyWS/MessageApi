from rest_framework import serializers
from .models import Message,MessageUser
from rest_framework.authtoken.models import Token

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender','receiver','subject','message','read','created_at']
