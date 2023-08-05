from django.contrib import admin

from .models import Category, Location, Post, Comment

admin.site.empty_value_display = "Не задано"


class PostInLine(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "pub_date",
        "author",
        "location",
        "category",
    )

    search_fields = ("title",)
    list_filter = ("is_published",)
    list_display_links = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
