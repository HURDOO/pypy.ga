from django.contrib import admin
from .models import Submit


class SubmitAdmin(admin.ModelAdmin):
    readonly_fields = ('type', 'code', 'submit_time', 'code_length', 'problem_id',
                       'user_id', 'stdin')
    # fields = ['result', 'time_usage', 'memory_usage', 'stdin', 'stdout',
    #           'last_case_idx'] + list(readonly_fields)

admin.site.register(Submit, SubmitAdmin)
