from django.urls import path
from . import views


urlpatterns = [
    path('articles/public/', views.PublicArticleList.as_view()),
    path('articles/private/', views.PrivateArticleList.as_view()),
    path('articles/<int:pk>/', views.ArticleAPIView.as_view()),
    path('articles/create/', views.ArticleCreateAPIView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
]