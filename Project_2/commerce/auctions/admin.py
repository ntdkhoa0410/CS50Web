from django.contrib import admin
from .models import User, Listing, Catergory, Bid, Comment
# Register your models here.

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Catergory)
admin.site.register(Bid)
admin.site.register(Comment)


