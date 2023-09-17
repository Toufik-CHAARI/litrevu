from django.contrib import admin
from articles.models import Ticket, Review, UserFollows

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "user")


admin.site.register(Ticket, ArticleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "headline")


admin.site.register(Review, ReviewAdmin)


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")


admin.site.register(UserFollows, UserFollowsAdmin)
