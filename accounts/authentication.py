from rest_framework.authentication import TokenAuthentication

from accounts.models import AuthToken


class MultipleTokenAuthentication(TokenAuthentication):
    model = AuthToken
