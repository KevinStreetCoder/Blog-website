from django import forms
from .models import comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments =forms.CharField(widget=forms.Textarea, required=False)

class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('name','email','body')
class SearchForm(forms.Form):
    query = forms.CharField()
    
    