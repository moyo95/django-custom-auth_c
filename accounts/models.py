from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model( email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user( email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        null=True, # nullを許容することで、既存のデータとの互換性を保つ
        blank=True
    )

    email = models.EmailField('メールアドレス', unique=True)
    first_name = models.CharField('姓', max_length=30,blank=True)
    last_name = models.CharField('名', max_length=150,blank=True)
    first_name_kana = models.CharField('かな',max_length=30, blank=True)
    last_name_kana = models.CharField('かな',max_length=30, blank=True)
    # address = models.CharField('住所', max_length=30, blank=True)
    postal_code = models.CharField('郵便番号',max_length=7, blank=True)
    address1 = models.CharField('住所1',max_length=255, blank=True)
    address2 = models.CharField('住所2',max_length=255, blank=True)
    tel = models.CharField('電話番号', max_length=30, blank=True)
    created = models.DateField('入会日', default=timezone.now)
    is_staff = models.BooleanField(
        'スタッフステータス',
        default=False,
        help_text='ユーザーが管理サイトにログインできるかどうかを指定します。',
    )
    is_active = models.BooleanField(
        'アクティブ',
        default=True,
        help_text=(
            'アカウントを削除する代わりに、非アクティブにするかどうかを指定します。'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def full_name(self):
        """姓と名を連結してフルネームを返す"""
        return f"{self.last_name} {self.first_name}"
    
    def get_full_name(self):
        """
        後方互換性やDjango Adminでの表示のために、
        get_full_nameメソッドも定義しておくのが一般的。
        """
        return self.full_name