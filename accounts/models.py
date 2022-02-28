from django.db import models
from django.contrib.auth.models import User
from six import MAXSIZE, python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from accounts.managers import AccountManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from docs.models import ProofPDF


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    mobile_number = models.CharField(max_length=13)
    proof = models.OneToOneField(ProofPDF, on_delete=models.DO_NOTHING, null=True, blank=True)
    institute_name = models.CharField(max_length=225)
    address = models.CharField(max_length=225, blank=True, null=True)
    degree = models.CharField(max_length=30, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = AccountManager()
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.email + ')'


class AuthToken(Token):
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)

    # Relation to user is a ForeignKey, so each user can have more than one token
    user = models.ForeignKey(
        Account,
        related_name="auth_tokens",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )