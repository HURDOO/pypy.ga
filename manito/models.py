import json

import yaml
from django.db import models
from problem import load


class ManitoAccount(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
        null=False,
        editable=False,
    )

    about_text = models.TextField(
        default=""
    )

    about_text_record = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder,
        default=list
    )

    photo = models.FileField(
        null=True
    )

    # 내가 함
    my_balance = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder,
        default=list
    )

    # 마니또가 해줌
    your_balance = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder,
        default=list
    )

    @classmethod
    def create(cls, user_id: int):
        account = ManitoAccount(id=user_id)
        account.save()
        return account

    def write_about(self, info: str) -> None:
        self.about_text_record.append(info)
        self.about_text = info
        self.save()


def get_manito_account(student_id: int) -> ManitoAccount:
    if student_id > 10000:
        student_id %= 100
    try:
        return ManitoAccount.objects.get(id=student_id)
    except ManitoAccount.DoesNotExist:
        return ManitoAccount.create(student_id)
