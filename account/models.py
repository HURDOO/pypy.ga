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

    last_submit = models.PositiveIntegerField(
        default=0,
        null=False
    )

    permissions = models.JSONField(
        null=False,
        default=list,
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder,
    )

    @classmethod
    def create(cls, user_id: int):
        account = Account(id=user_id)
        account.save()
        return account

    def add_submit(self, problem_id: int, submit_id: int, score: int) -> None:
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

        delta = score - prev_score
        self.score += delta
        if delta > 0:
            self.last_submit = submit_id
        self.save()

    def view_code(self, problem_id):
        if str(problem_id) not in self.submits:
            self.add_submit(problem_id, -2, 0)
        self.submits[str(problem_id)]['view_code'] = True
        self.save()

    def grant_permission(self, perm: str) -> None:
        if perm not in self.permissions:
            self.permissions.append(perm)
            self.save()

    def revoke_permission(self, perm: str) -> None:
        if perm in self.permissions:
            self.permissions.remove(perm)
            self.save()


def handle_login(user_id: int) -> Account:
    user = Account.objects.filter(id=user_id)
    if user.exists():
        return user.first()
    else:
        return Account.create(user_id=user_id)
