from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


# Create your models here.
class Team(models.Model):
    status = models.BooleanField(default=False)
    participation = models.ManyToManyField(User, blank=True)

class UserPortfolio(models.Model):
    # 수정: 한개만 저장할 수 있도록!!
    author = models.ForeignKey(User, on_delete=True)
    content = MarkdownxField()
    def get_markdown_content(self):
        return markdown(self.content)


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'

class Project(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    status = models.BooleanField(default=False)

    start_date = models.DateField()
    end_date = models.DateField()
    prj_image = models.ImageField(upload_to="blog/project/%y/%m/%d", blank=True)
    author = models.ForeignKey(User, on_delete=True)
    participation = models.ForeignKey(Team, blank=True, on_delete=models.SET(None), null=True)
    category = models.ManyToManyField(Category, blank=True) # Part

    def __str__(self):
        return "{}".format(self.title)
    def get_absolute_url(self):
        return '    /app/{}/'.format(self.pk)
    def get_markdown_content(self):
        return markdown(self.content)

class Tag(models.Model):
    title = models.TextField()
    project = models.ForeignKey(Project, on_delete=True)
    category = models.ForeignKey(Category, on_delete=True)
    user = models.ForeignKey(User, on_delete=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'tags'

class Todo(models.Model):
    content = models.TextField()
    status = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=True)
    category = models.ForeignKey(Category, on_delete=True)
    # tag = models.ForeignKey(Tag, on_delete=False, blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{}".format(self.content)

