from django import forms

from .models import Project,Category, Todo

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'content', 'start_date', 'end_date', 'category', 'prj_image']

        def __init__(self, *args, **kwargs):
            super(ProjectForm, self).__init__(*args, **kwargs)
            self.fields["category"].widget = forms.widgets.CheckboxSelectMultiple()
            self.fields["category"].queryset = Category.objects.all()


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['content', 'category', 'project', 'tag', 'end_date']
