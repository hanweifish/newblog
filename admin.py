from django.contrib import admin

from newblog.models import Blog, Tag
# from newblog.form import UserForm

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'pwd', 'email')
#     search_fields = ('name',)
#     # form = UserForm
 
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'user', 'published_time')
    list_filter = ('published_time',)
    date_hierarchy = 'published_time'
    ordering = ('-published_time',)
    filter_horizontal = ('tags',)


# admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)

# Register your models here.
