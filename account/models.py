from django.db import models
from pypyga.settings import conf
import re

EMAIL_REGEX = fr"{conf['google']['email_regex']}"


class AccountModel(models.Model):

    def __init__(self, user_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = user_id

    id = models.PositiveIntegerField(primary_key=True, null=False, default=10000)


def handle_login(email: str) -> AccountModel:
    user_id = get_id(email)
    try:
        return AccountModel.objects.get(id=user_id)
    except AccountModel.DoesNotExist:
        return AccountModel(user_id=user_id)


def get_id(email: str) -> int:
    regex = re.compile(EMAIL_REGEX)
    pattern = regex.match(email)
    return pattern.group(1)
