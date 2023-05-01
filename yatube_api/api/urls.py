from django import views
from django.urls import include, path
from rest_framework import routers

from .views import (CommentsViewSet, FollowListAndCreate, GroupsViewSet,
                    PostsViewSet)

router = routers.DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')
router.register(
    r'^posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register('groups', GroupsViewSet, basename='groups')


urlpatterns = [
    path('v1/follow/', FollowListAndCreate.as_view()),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
