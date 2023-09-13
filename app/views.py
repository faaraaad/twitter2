import rest_framework.pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Post, CustomUser
from .serializers import PostSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import pagination
from redis import Redis
import pickle


# class PostPagination(pagination.CursorPagination):
#     page_size = 5
#     ordering = "-create_at"

redis_connection = Redis(host='localhost', port=63, db=4)


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # pagination_class = PostPagination

    def list(self, request, *args, **kwargs):
        if szd_data := redis_connection.lrange(f"user-{request.user.id}", 0, -1):
            data = pickle.loads(szd_data[0])
            print(data, request.user.id)
            return Response(data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            pickle_szd_data = pickle.dumps(serializer.data)
            redis_connection.lpush(f"user-{request.user.id}", pickle_szd_data)
        return Response(serializer.data)

    def get_queryset(self):
        posts = self.request.user.get_feed_of_user()
        return posts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UsersView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @action(detail=True, methods=["POST"])
    def follow(self, request, pk=None):
        user = self.request.user
        user.follow(pk)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    @action(detail=False)
    def followings(self, request):
        szd_data = UserSerializer(instance=request.user.get_following_of_user(), many=True)
        return Response(szd_data.data)

    @action(detail=False)
    def followers(self, request):
        szd_data = UserSerializer(instance=request.user.get_follower_of_user(), many=True)
        return Response(szd_data.data)

    @action(detail=True, methods=["POST"])
    def unfollow(self, request, pk=None):
        self.request.user.unfollow(pk)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class Public(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class Who_Am_I(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"id": request.user.id,
                         "username": request.user.username})