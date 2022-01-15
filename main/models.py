from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя
        """
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя
        """
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def validate_lon(value):
    """
    Валидация значения longitude

    Если значение валидно, возвращает None
    Если значение невалидно, вызывает ValidationError
    """
    if -180 < value < 180:
        return
    else:
        raise ValidationError(
            'Допустимый диапазон значений от -180 до 180')


def validate_lat(value):
    """
    Валидация значения latitude

    Если значение валидно, возвращает None
    Если значение невалидно, вызывает ValidationError
    """
    if -90 < value < 90:
        return
    else:
        raise ValidationError(
            'Допустимый диапазон значений от -90 до 90')


class User(PermissionsMixin, AbstractBaseUser):
    """
    Модель пользователя
    """
    MAN = 'М'
    WOMAN = 'Ж'
    GENDER_CHOICES = [
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='%Y/%m/')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    is_staff = models.BooleanField(default=False)
    likes = models.ManyToManyField('self', symmetrical=False, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[validate_lon], blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, validators=[validate_lat], blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Возвращает полное имя пользователя
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def has_coords(self):
        """
        Проверяет заполнены ли поля longitude и latitude

        Если заполнены оба, возвращает True, иначе False
        """
        if self.longitude and self.latitude:
            return True
        return False
