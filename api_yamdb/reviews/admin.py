from django.contrib import admin

from reviews.models import Comment, Review


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "review")
    search_fields = ("author",)
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "title")
    search_fields = ("author",)
    empty_value_display = "-пусто-"


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
