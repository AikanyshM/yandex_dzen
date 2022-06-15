from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import PostSerializer, UserSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from .models import Post, Comment
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsAdminorAuthenticated

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    authentification_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.validated_data['is_staff'] = False
        serializer.save()


class AdminCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]
    authentification_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.validated_data['is_staff'] = True
        serializer.save()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminorAuthenticated, ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_queryset(self):
        published_date_before = self.request.GET.get('before')
        published_date_after = self.request.GET.get('after')
        part_header = self.request.GET.get('part_header')
        if published_date_after:
            queryset = self.queryset.filter(published_date__lte = published_date_after)
        if published_date_before:
            queryset = self.queryset.filter(published_date__gt = published_date_before)
        if part_header:
            queryset = self.request.filter(header__icontains = part_header)
            return queryset
        


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminorAuthenticated, ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        comments = Comment.objects.filter(user = user)
        posts = Post.objects.filter(comment__in = comments)
        return posts 
        
