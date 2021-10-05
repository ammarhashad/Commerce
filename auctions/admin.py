from django.contrib import admin
from .models import User,Listings,Bid,Comment

# Register your models here.
class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "starting_bid","user","close")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id","bid","bid_date")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment","comment_date")


admin.site.register(User)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
