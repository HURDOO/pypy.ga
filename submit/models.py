import asyncio
import json

from django.db import models
from django.utils import timezone
from .consumers import update_status
from django.utils.translation import gettext_lazy as _


class SubmitType(models.TextChoices):
    TEST = 'T'
    GRADE = 'G'


def getSubmitType(_type: str) -> SubmitType:
    if _type == '테스트 실행':
        return SubmitType.TEST
    elif _type == '코드 제출':
        return SubmitType.GRADE


class ResultType(models.TextChoices):
    ACCEPTED = 'AC', _('✅ 맞았습니다!!')  # 정답
    WRONG_ANSWER = 'WA', _('❌ 틀렸습니다')  # 오답
    COMPLETE = 'CP', _('✅ 실행 완료')  # 실행 완료 (type = Test)

    TIME_LIMIT = 'TLE', _('⏳ 시간 초과')  # 시간 초과
    MEMORY_LIMIT = 'MLE', _('💣 메모리 초과')  # 메모리 초과
    OUTPUT_LIMIT = 'OLE', _('📝 출력 초과')  # 출력 초과

    RUNTIME_ERROR = 'RTE', _('💥 오류 발생')  # 런타임 에러
    # COMPILE_ERROR = 'CE',  # 컴파일 에러

    PREPARE = 'PRE', _('🚩 준비 중')  # 채점 준비 중
    ONGOING = 'ON', _('🔁 채점 중')  # 채점 중

    INTERNAL_ERROR = 'IE', _('⚠️내부 오류'),  # 내부 오류


class Submit(models.Model):

    @classmethod
    def create(cls,
               _type: SubmitType,
               _problem_id: int,
               _user_id: int,
               _code: str,
               _input_data: str = None
               ):
        _submit_time = timezone.datetime.now()
        submit = Submit(type=_type, problem_id=_problem_id, user_id=_user_id, code=_code, submit_time=_submit_time,
                        stdin=_input_data)
        if _input_data is not None:
            submit.input_data = _input_data
        submit.code_length = len(_code)
        submit.save()

        return submit

    type = models.CharField(
        max_length=1,
        choices=SubmitType.choices,
        null=False,
        editable=False
    )

    code = models.TextField(
        null=False,
        editable=False
    )

    result = models.CharField(
        max_length=3,
        choices=ResultType.choices,
        default=ResultType.PREPARE,
        null=False
    )
    # get_result_display() to get display name

    time_usage = models.PositiveIntegerField(
        null=True  # result = ONGOING
    )  # ms

    memory_usage = models.PositiveIntegerField(
        null=True  # result = ONGOING
    )  # kb

    submit_time = models.DateTimeField(
        null=False,
        editable=False
    )

    code_length = models.PositiveIntegerField(
        null=False,
        editable=False
    )

    problem_id = models.PositiveIntegerField(
        null=False,
        editable=False
    )

    user_id = models.PositiveIntegerField(
        null=False,
        editable=False
    )

    stdin = models.TextField(
        null=True,  # type = Grade
        editable=False
    )

    stdout = models.TextField(
        null=True  # result = ONGOING
    )

    stderr = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder,
        null=True  # result = ONGOING or no error
    )

    last_case_idx = models.PositiveIntegerField(
        null=True  # result = ONGOING or ACCEPTED
    )

    def start(self):
        self.result = ResultType.ONGOING
        self.save()
        self.send_websocket({
            'type': 'progress',
            'progress': 0
        }, close=False)

    def case_done(self, percentage: int):
        self.send_websocket({
            'type': 'progress',
            'progress': int(percentage)
        }, close=False)

    def end(self,
            _result: ResultType,
            _time_usage: int,
            _memory_usage: int,
            _stdout: str,
            _stderr: dict = None,
            _last_case_idx: int = None
            ):
        self.result, self.time_usage, self.memory_usage, self.stdout, self.stderr, self.last_case_idx \
            = _result, _time_usage, _memory_usage, _stdout, _stderr, _last_case_idx
        self.save()
        self.send_websocket({
            'type': 'reload'
        }, close=True)

    def internal_error(self, _stderr: str):
        self.result, self.stderr = ResultType.INTERNAL_ERROR, _stderr
        self.save()
        self.send_websocket({
            'type': 'reload',
        }, close=True)

    def send_websocket(self, data: dict, close: bool) -> None:
        asyncio.run(update_status(self.id, data, close))
