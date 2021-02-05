from django.contrib import admin
from .models import Post, comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    #fields=('title','author','publish','slug')

@admin.register(comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter =('active','created','body')
    search_field = ('name','email','body')

