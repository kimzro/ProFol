from django.contrib import admin
from .models import Project, Category, Todo, UserPortfolio, Tag, Team

# Register your models here.

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Todo)
admin.site.register(Tag)
admin.site.register(UserPortfolio)
admin.site.register(Team)