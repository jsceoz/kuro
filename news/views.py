from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, filters
from news.serializers import UserSerializer, GroupSerializer, ArticleSerializer, CategorySerializer, ViewSerializer, LikeSerializer
from .models import Article, Category, View, Like
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
from django.http import JsonResponse
import random


def get_user_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return JsonResponse({'ip': ip})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [TokenHasReadWriteScope, ]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ArticleList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-id')
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, TokenHasReadWriteScope)
    # authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category', 'title')
    search_fields = ('title',)


class CategoryViewsSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, TokenHasReadWriteScope)
    # authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ViewViewSet(viewsets.ModelViewSet):

    queryset = View.objects.all()
    serializer_class = ViewSerializer
    permission_classes = (AllowAny,)


class LikeViewSet(viewsets.ModelViewSet):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (AllowAny,)


