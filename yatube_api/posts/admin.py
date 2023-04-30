from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'created', 'post', 'author')
    search_fields = ('author', 'post', 'text')
    list_filter = ('author', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    list_filter = ('following',)
    empty_value_display = '-пусто-'
