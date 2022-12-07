from django.http import JsonResponse
from .models import Message
from .serializers import MessageSerializer
from rest_framework import status,generics,viewsets
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from rest_framework.decorators import action


class MessageAll(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class=[MessageSerializer]
    
    def get_queryset(self,request=None,pk=None):
        usertoken=Token.objects.get(key=self.request.auth)
        if pk == "unread":
            queryset=Message.objects.filter(Q(receiver=usertoken.user_id) & Q(read=False))
            return queryset
        if pk:
            queryset=Message.objects.filter(Q(sender_id=usertoken.user_id) & Q(id=pk))
            if not queryset:
                queryset=Message.objects.filter(Q(receiver=usertoken.user_id) & Q(id=pk)).update(read=True)
                if queryset:
                    queryset=Message.objects.filter(Q(receiver=usertoken.user_id) & Q(id=pk))
            return queryset
        queryset=Message.objects.filter(Q(sender_id=usertoken.user_id) | Q(receiver=usertoken.user_id))
        return queryset

    def list(self,request:Request):
        messages=self.get_queryset(request)
        if not messages:
            return JsonResponse({'status':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=MessageSerializer(messages, many=True)
        return JsonResponse({'status':f'{str(request.user.id)} Logged in','messages':serializer.data},status=status.HTTP_200_OK)
    

    def create(self,request:Request):
        usertoken=Token.objects.get(key=request.auth)
        newdict={**request.data,"sender":usertoken.user_id}
        serializer= MessageSerializer(data=newdict)
        if not serializer.is_valid():
            return JsonResponse({'status':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer.save()
        return JsonResponse({'status':f'{str(usertoken.user_id)} Logged in, Message Created',"messages":serializer.data},status=status.HTTP_201_CREATED)
    

    def update(self, request,pk=None):
        message=self.get_queryset(request,pk=pk)
        if not message:
            return JsonResponse({'status':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=MessageSerializer(message, many=True)
        return JsonResponse({'message':serializer.data},status=status.HTTP_200_OK)

    
    def destroy(self, request,pk=None):
        message=self.get_queryset(request,pk=pk)
        if not message:
            return JsonResponse({'status':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        message.delete()
        return JsonResponse({'status':"Deleted Succses"},status=status.HTTP_200_OK)


    @action(detail=True,methods=['get'])
    def unread(self,request):
        messages=self.get_queryset(request,pk='unread')
        if not messages:
            return JsonResponse({'status':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer=MessageSerializer(messages, many=True)
        return JsonResponse({'status':f'{str(request.user.id)} Logged in','messages':serializer.data},status=status.HTTP_200_OK)



# pep8

