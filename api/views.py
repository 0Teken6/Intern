from .models import Article
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import generics
from .serializers import ArticleSerializer, RegisterSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwnerOrReaderOnly, IsAuthorOrSuperUser

from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status


class PublicArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(is_private=False)


class PrivateArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(is_private=True)
    permission_classes = (IsAuthenticated, )


class ArticleCreateAPIView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (IsAuthorOrSuperUser, IsAuthenticated)
    
    def perform_create(self, serializer):
        if self.request.user.role != "author":
            raise PermissionDenied('You do not have permission to create articles.')
        
        serializer.save(author=self.request.user)


class ArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (IsOwnerOrReaderOnly, )

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class RegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "You are already registered and logged in."}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class LoginAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response({"message": "You are logged in"})
    

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})
    