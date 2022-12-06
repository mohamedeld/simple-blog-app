from django.contrib import admin
from blog_app.models import Blog, Author,Tag,Comment
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_filter = ("author","tag","date",)
    list_display= ("title","date","author",)
    prepopulated_fields= {"slug":("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name","post")

admin.site.register(Blog,BlogAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)