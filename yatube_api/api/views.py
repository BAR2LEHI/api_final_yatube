from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post
from rest_framework import filters, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostsViewSet(viewsets.ModelViewSet):
    """
    Viewset для обработки всех
    http-запросов к эндпоинту api/v1/posts/
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Viewset для обработки всех
    http-запросов к эндпоинту api/v1/<id:post>/comments/
    """
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly, )

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, post=self.get_post())


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset для обработки всех
    http-запросов к эндпоинту api/v1/groups/
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowListAndCreate(ListCreateAPIView):
    """Viewset для обработки всех
    http-запросов к эндпоинту api/v1/follow/
    """
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.save(user=self.request.user)
