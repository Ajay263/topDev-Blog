from django import forms
from .models import Email,Comment,Contact

class EmailPostForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),   
            'email':forms.EmailInput(attrs={'class':'form-control'}), 
            'to':forms.TextInput(attrs={'class':'form-control'}), 
            'comments':forms.Textarea(attrs={'class':'form-control'}), 
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),   
            'email':forms.EmailInput(attrs={'class':'form-control'}), 
            'body':forms.Textarea(attrs={'class':'form-control'}), 
        }

class SearchForm(forms.Form):
      query = forms.CharField()
          
class Contactform(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),   
            'email':forms.EmailInput(attrs={'class':'form-control'}), 
            'subject':forms.TextInput(attrs={'class':'form-control'}), 
            'Message':forms.Textarea(attrs={'class':'form-control'}), 
        }