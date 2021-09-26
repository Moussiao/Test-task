from django.contrib import admin
from .models import Company, UserAddress, User, PostCategory, Post


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Company)
admin.site.register(UserAddress)
admin.site.register(User)
admin.site.register(Post)
