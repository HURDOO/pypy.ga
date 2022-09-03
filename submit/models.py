from django.db import models
from django.utils import timezone


class SubmitType(models.TextChoices):
    TEST = 'T'
    GRADE = 'G'


def getSubmitType(_type: str) -> SubmitType:
    if _type == '테스트 실행':
        return SubmitType.TEST
    elif _type == '코드 제출':
        return SubmitType.GRADE


class ResultType(models.TextChoices):
    ACCEPTED = 'AC',  # 정답
    WRONG_ANSWER = 'WA',  # 오답
    COMPLETE = 'CP'  # 실행 완료 (type = Test)

    TIME_LIMIT = 'TLE',  # 시간 초과
    MEMORY_LIMIT = 'MLE',  # 메모리 초과
    OUTPUT_LIMIT = 'OLE',  # 출력 초과

    RUNTIME_ERROR = 'RTE',  # 런타임 에러
    COMPILE_ERROR = 'CE',  # 컴파일 에러

    PREPARE = 'PRE',  # 채점 준비 중
    ONGOING = 'ON',  # 채점 중

    INTERNAL_ERROR = 'IE',  # 내부 오류


class Submit(models.Model):

    @classmethod
    def create(cls,
               _type: SubmitType,
               _problem_id: int,
               _user_id: int,
               _code: str,
               _submit_time: str,
               _input_data: str = None
               ):
        __submit_time = timezone.datetime.strptime(_submit_time.split('.')[0], "%Y-%m-%dT%H:%M:%S")
        submit = Submit(type=_type, problem_id=_problem_id, user_id=_user_id, code=_code, submit_time=__submit_time)
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

    stderr = models.TextField(
        null=True  # result = ONGOING or no error
    )

    last_case_idx = models.PositiveIntegerField(
        null=True  # result = ONGOING or ACCEPTED
    )

    def start(self):
        self.result = ResultType.ONGOING
        self.save()

    def end(self,
            _result: ResultType,
            _time_usage: int,
            _memory_usage: int,
            _stdout: str,
            _stderr: str = None
            ):
        self.result, self.time_usage, self.memory_usage, self.stdout, self.stderr \
            = _result, _time_usage, _memory_usage, _stdout, _stderr
        self.save()

    def internal_error(self):
        self.result = ResultType.INTERNAL_ERROR
        self.save()
