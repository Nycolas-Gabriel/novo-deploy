from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import CustomUser  
from .models import Item
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser  
        fields = ('username', 'email', 'password1', 'password2', 'profile_image')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'descricao']
        
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
