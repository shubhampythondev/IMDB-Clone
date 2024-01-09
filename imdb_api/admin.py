from django.contrib import admin
from .models import StreamPlatform, Watchlist, Review

# Register your models here.

admin.site.register(StreamPlatform)
admin.site.register(Watchlist)
admin.site.register(Review)
