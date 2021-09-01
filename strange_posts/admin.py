from django.contrib import admin
from .models import Company, UserAddress, User, Post

admin.site.register(Company)
admin.site.register(UserAddress)
admin.site.register(User)
admin.site.register(Post)
