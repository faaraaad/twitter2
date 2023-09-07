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


class PostPagination(PageNumberPagination):
    page_size = 5


class PostView(ModelViewSet):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        posts = Post.objects.filter(
            author__in=self.request.user.followings.all()).order_by("create_at")
        return posts

    # def filter_queryset(self, queryset):
    #     posts =  Post.objects.filter(author__in=self.request.user.followings.all())
    #     return posts
        # user = CustomUser.objects.get(pk=self.request.user.id)
        # return user.get_feed_of_user()

    def perform_create(self, serializer):
        user = CustomUser.objects.get(pk=self.request.user.id)
        serializer.save(author=user)


class UsersView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @action(detail=True, methods=["GET"])
    def follow(self, request, pk=None):
        self.request.user.follow(pk)
        return Response(f"you followed {pk}")

    @action(detail=False)
    def followings(self, request):
        user = self.get_object()
        followings = user.get_following_of_user()
        szd_data = UserSerializer(instance=followings, many=True)
        return Response(szd_data.data)

    @action(detail=True, methods=["GET"])
    def unfollow(self, request, pk=None):
        self.request.user.unfollow(pk)
        return Response(f"you unfollowed {pk}")


class Public(APIView):
    def get(self, request):
        return Response('this is ok')
