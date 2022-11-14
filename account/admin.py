from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

    actions = ['modify_permission']

    @admin.action(description='권한 변경')
    def modify_permission(self, request, queryset):
        if 'submit' in request.POST:
            for account in queryset:
                perm = request.POST['perm']

                if request.POST['mode'] == 'grant':
                    account.grant_permission(perm)
                    self.message_user(request,
                                      f'Granted "{perm}" for {len(queryset)} users.')
                else:
                    account.revoke_permission(request.POST['perm'])
                    self.message_user(request,
                                      f'Revoked "{perm}" for {len(queryset)} users.')

            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'admin/modify_permission.html', {
            'action': 'modify_permission',
            'orders': queryset
        })


admin.site.register(Account, AccountAdmin)
