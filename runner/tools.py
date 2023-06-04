from . import runner
from submit.models import Submit, SubmitType


def regrade(from_id: int, to_id: int) -> None:
    for submit_id in range(from_id, to_id+1):
        submit = Submit.objects.get(id=submit_id)

        runner.register_submit(submit.id, submit.problem_id,
                               submit.code, submit.type, submit.stdin)

    return
