from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from pypyga.settings import conf
import re

EMAIL_REGEX = fr"{conf['google']['email_regex']}"
regex = re.compile(EMAIL_REGEX)


class Account(models.Model):

    id = models.PositiveIntegerField(primary_key=True, null=False, editable=False, default=10000)

    @classmethod
    def create(cls, user_id: int):
        account = Account(id=user_id)
        account.save()
        return account


def handle_login(email: str) -> Account:
    user_id = get_id(email)
    user = Account.objects.filter(id=user_id)
    if user.exists():
        return user.first()
    else:
        return Account.create(user_id=user_id)


def get_id(email: str) -> int:
    pattern = regex.match(email)
    return pattern.group(1)
