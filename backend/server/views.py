from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer

# Create your views here.

class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self,request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        server_id = request.query_params.get("server_id")


        if by_user or server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category__name = category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member = user_id)

        if server_id:
            try:
                self.queryset = self.queryset.filter(id = server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail = f"Server with Id {server_id} does not exists")
            except ValueError:
                raise ValidationError(detail=f"Server Value Error")


        if qty:
            self.queryset = self.queryset[: int(qty)]

    
        serializer = ServerSerializer(self.queryset, many = True)
        return Response(serializer.data)