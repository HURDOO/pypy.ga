import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from pypyga.settings import conf
import re

EMAIL_REGEX = fr"{conf['google']['email_regex']}"
regex = re.compile(EMAIL_REGEX)


class Account(models.Model):

    id = models.PositiveIntegerField(
        primary_key=True,
        null=False,
        editable=False,
    )

    score = models.PositiveIntegerField(
        default=0,
        null=False,
    )

    submits = models.JSONField(
        null=False,
        default=dict,
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder,
    )

    @classmethod
    def create(cls, user_id: int):
        account = Account(id=user_id)
        account.save()
        return account

    def add_submit(self, problem_id: int, submit_id: int, score: int):
        problem_id = str(problem_id)
        if problem_id in self.submits:
            prev = self.submits[problem_id]
            if prev['score'] > score:
                return
            prev_score = prev['score']
        else:
            prev_score = 0

        self.submits[problem_id] = {
            'submit_id': submit_id,
            'score': score
        }

        self.score += score - prev_score
        self.save()


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
