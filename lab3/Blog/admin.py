from __future__ import annotations

from django.contrib import admin
from .models import BlogUser, Post, Comment, File, Block


@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.user:
            return True
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user"]
    search_fields = ["title", "content"]
    list_filter = ["created_at"]

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.user.user:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (
                obj and not Block.objects.filter(blocker__user=obj.user.user, blocked__user=request.user).exists()):
            return True
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "creation_date"]

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (
                obj and not Block.objects.filter(blocker__user=obj.post.user.user, blocked__user=request.user).exists()):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.post.user.user:
            return True
        return False


@admin.register(File)
class FileAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.post.user.user:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (
                obj and not Block.objects.filter(blocker__user=obj.user.user, blocked__user=request.user).exists()):
            return True
        return False

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.blocker.user:
            return True
        return False
