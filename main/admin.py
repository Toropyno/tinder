from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    Форма для создания новых пользователей. Включает все обязательные поля
    и повторяющееся поле пароля
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'photo', 'gender')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Форма для изменения данных пользователя
    """
    password = ReadOnlyPasswordHashField(help_text='<a href="../password/">Сменить пароль</a>')

    class Meta:
        model = User
        fields = ('email', 'password')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Представление модели User в админ панели
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'id', 'longitude', 'latitude')
    list_filter = ('email',)
    list_editable = ('longitude', 'latitude')
    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'photo', 'gender')}),
        ('Location', {'fields': ('longitude', 'latitude')}),
        ('Likes', {'fields': ('likes',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'user_permissions', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'photo',
                'gender',
            ),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ('likes',)
