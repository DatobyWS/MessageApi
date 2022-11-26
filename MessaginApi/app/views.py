from django.http import JsonResponse
from .models import MessageUser,Message
from django.contrib.auth import authenticate
from .serializers import MessageSerializer
from rest_framework import status,generics
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

class MessageAll(generics.GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request:Request):
        usertoken=Token.objects.get(key=request.auth)
        massage_user=MessageUser.objects.get(id=request.user.id)
        if usertoken.user_id == massage_user.id:
            messages=Message.objects.filter(Q(sender_id=usertoken.user_id) | Q(receiver=usertoken.user_id))
            if messages:
                serializer=MessageSerializer(messages, many=True)
                return JsonResponse({'status':f'{str(usertoken.user_id)} Logged in','messages':serializer.data},status=status.HTTP_200_OK)
            else:
                return JsonResponse({'status':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'status':'Faild to Logged in'},status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request:Request):
        user_name=request.data['username']
        password=request.data['password']
        senderid=request.data['sender']
        serializer= MessageSerializer(data=request.data)
        user=authenticate(username=user_name,password=password)
        if user is not None:
            usertoken=Token.objects.get(key=request.auth)
            massage_user=MessageUser.objects.get(id=user.id)
            if usertoken.user_id == massage_user.id and usertoken.user_id == senderid :
                if serializer.is_valid():
                    serializer.save()
                return JsonResponse({'status':f'{str(usertoken.user_id)} Logged in, Message Created',"messages":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'status':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
            
        if user is None:
            return JsonResponse({'status':'Your User name or Password are worng! Please Try Again!'},status=status.HTTP_404_NOT_FOUND)
    
class MessageOne(generics.GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self,request:Request,pk):
        usertoken=Token.objects.get(key=request.auth)
        massage_user=MessageUser.objects.get(id=request.user.id)
        if usertoken.user_id == massage_user.id:
            message=Message.objects.filter(Q(id=pk) & Q(receiver=usertoken.user_id)).update(read=True)
            if message:
                message=Message.objects.filter(id=pk)
                serializer=MessageSerializer(message, many=True)
                return JsonResponse({'message':serializer.data},status=status.HTTP_200_OK)
            if message == 0:
                message=Message.objects.filter(Q(id=pk) & Q(sender_id=usertoken.user_id))
                if message:
                    serializer=MessageSerializer(message, many=True)
                    return JsonResponse({'message':serializer.data},status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'status':"Not Found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'status':'Faild to Logged in'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request:Request,pk):
        usertoken=Token.objects.get(key=request.auth)
        massage_user=MessageUser.objects.get(id=request.user.id)
        if usertoken.user_id == massage_user.id:
            message=Message.objects.filter(Q(id=pk) & Q(sender_id=usertoken.user_id) | Q(id=pk) & Q(receiver=usertoken.user_id))
            if message:
                message.delete()
                return JsonResponse({'status':"Deleted Succses"},status=status.HTTP_200_OK)
            else:
                return JsonResponse({'status':"Not Found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'status':'Faild to Logged in'},status=status.HTTP_404_NOT_FOUND)

class MessageNotRead(generics.GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request:Request):
        usertoken=Token.objects.get(key=request.auth)
        massage_user=MessageUser.objects.get(id=request.user.id)
        if usertoken.user_id == massage_user.id:
            message=Message.objects.filter(Q(receiver=usertoken.user_id) & Q(read=False))
            if message:
                serializer=MessageSerializer(message, many=True)
                return JsonResponse({'message':serializer.data},status=status.HTTP_200_OK)
            else:
                return JsonResponse({'status':"Not Found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'status':'Faild to Logged in'},status=status.HTTP_404_NOT_FOUND)
