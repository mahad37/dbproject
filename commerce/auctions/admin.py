from django.contrib import admin
from .models import Listings, User, Comments, Bids, Transactions

# Register your models here.

admin.site.register(Listings)
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Transactions)
