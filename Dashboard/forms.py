from django import forms
from .models import task

class taskform(forms.ModelForm):
    class Meta:
        model = task
        fields = ['Attribute', 'Task', 'Duration', 'Predecessors', 'RequiredRT', 'Staffid']

class progressform(forms.ModelForm):
    class Meta:
        model = task
        fields = ['Progress']
        widgets = {
            'Progress': forms.Select(attrs={'class': 'form-control'})  # Ensure correct widget class
        }

    def __init__(self, *args, **kwargs):
        super(progressform, self).__init__(*args, **kwargs)
        self.fields['Progress'].widget.attrs.update({'class': 'form-control'})
