from django.contrib import admin
from .models import AccountModel


class AccountModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)



admin.site.register(AccountModel, AccountModelAdmin)
