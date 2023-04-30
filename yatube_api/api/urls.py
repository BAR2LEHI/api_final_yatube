from django.urls import include, path
from rest_framework import routers

from .views import CommentsViewSet, FollowViewSet, GroupsViewSet, PostsViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(
    r'^posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register(r'groups', GroupsViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
