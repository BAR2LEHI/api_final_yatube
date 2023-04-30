import base64

from django.core.files.base import ContentFile
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Сериализатор поля изображения декодировка base64"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, string = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(string), name='temp.' + ext)
            return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор данных постов"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор данных комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор данных групп"""

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор данных подписки"""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following',)
        model = Follow

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError('Подписка на '
                                              'самого себя недопустима.')
        if Follow.objects.filter(user=self.context['request'].user,
                                 following=value).exists():
            raise serializers.ValidationError('Вы уже подписаны'
                                              ' на данного пользователя.')
        return value
