from django.forms import ModelForm
from django import forms
from .models import Plant
from .models import PlantPhoto
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import ArchiveNote


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'

class PlantPhotoForm(forms.ModelForm):
    photo = MultipleFileField()
    class Meta:
        model = PlantPhoto
        fields = ('photo',)
        
    
class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
class ArchiveNoteForm(forms.ModelForm):
    class Meta:
        model = ArchiveNote
        fields = '__all__'
        widgets = {
            'plant': forms.TextInput(attrs={'readonly': True}),
        }
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется. Пожалуйста, используйте другой email.')
        return email
