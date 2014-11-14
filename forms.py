from django.forms import ModelForm, PasswordInput
from newblog.models import Blog, Tag
from django import forms
from django.contrib.auth.models import User

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         widgets = {
#             'password': PasswordInput(),
#         }



 
class BlogForm(forms.Form):
    title = forms.CharField(required=True, label='title', max_length=100)
    content = forms.CharField(widget=forms.Textarea())

class TagForm(forms.Form):
    tag_name = forms.CharField()


class LoginForm(forms.Form):  
    username = forms.CharField(  
        required=True,  
        label=u"username",  
        error_messages={'required': 'Please Input Username'},  
        widget=forms.TextInput(  
            attrs={  
                'placeholder':u"Username",  
            }  
        ),  
    )      
    password = forms.CharField(  
        required=True,  
        label=u"password",  
        error_messages={'required': u'Please Input Password'},  
        widget=forms.PasswordInput(  
            attrs={  
                'placeholder':u"Password",  
            }  
        ),  
    )     
    def clean(self):  
        if not self.is_valid():  
            raise forms.ValidationError(u"Please input username and password")  
        else:  
            cleaned_data = super(LoginForm, self).clean()  

