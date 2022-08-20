from django.db import models
import re


class AccountModel(models.Model):

    def __init__(self, email: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = gen_id(email)

    id = models.PositiveIntegerField(primary_key=True)


def gen_id(email: str):
    regex = re.compile(r"^js22-(\d+)@sonline20\.sen\.go\.kr$")
    pattern = regex.match(email)
    return pattern.group(1)
