from django.contrib import admin
from .models import ManitoAccount


class ManitoAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(ManitoAccount, ManitoAdmin)
