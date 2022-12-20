from django.shortcuts import render, redirect
from account.info import get_data, get_user_id
from . import models
from .load import student_name, first_day_manito


def main(request):
    data = get_data(request.session)
    student_id = get_user_id(request.session)
    if student_id is None:
        return redirect('/')
    data['name'] = student_name[str(student_id % 100)]
    data['first_manito'] = student_name[str(first_day_manito[str(student_id % 100)])]
    return render(request, 'manito.html', data)


def about(request):
    data = get_data(request.session)
    student_id = get_user_id(request.session)
    if student_id is not None:
        if request.POST:
            info = request.POST['info']
            models.get_manito_account(first_day_manito[str(student_id % 100)]).write_about(info)

        data['first_manito'] = student_name[str(first_day_manito[str(student_id % 100)])]

    lst = []
    for manito in models.ManitoAccount.objects.all():
        lst.append({
            'name': student_name[str(manito.id)],
            'text': manito.about_text
        })
    data['manito'] = lst
    # print(lst)
    return render(request, 'about.html', data)


def balance(request):
    data = get_data(request.session)
    data['show_form'] = False
    student_id = get_user_id(request.session)

    if student_id is not None:
        manito_num = first_day_manito[str(student_id % 100)]
        my_account = models.get_manito_account(student_id)
        if request.POST:
            my, your = {}, {}
            for suffix in ['food', 'phone', 'ramen', 'money', 'chocopie']:
                my['my_' + suffix] = request.POST['my_' + suffix]
                your['your_' + suffix] = request.POST['your_' + suffix]

            my_account.my_balance = my
            my_account.save()

            manito_account = models.get_manito_account(manito_num)
            manito_account.your_balance = your
            manito_account.save()

            my_account.gen_balance()
            manito_account.gen_balance()

        data['first_manito'] = student_name[str(manito_num)]
        data['show_form'] = not bool(len(my_account.my_balance))

    lst = []
    for manito in models.ManitoAccount.objects.all():
        lst.append({
            'name': student_name[str(manito.id)],
            'balance': manito.balance,
            'choice': manito.my_balance
        })
    data['manito'] = lst
    # print(lst)
    return render(request, 'balance.html', data)


def photo(request):
    data = get_data(request.session)
    student_id = get_user_id(request.session)
    if student_id is not None:
        manito_num = first_day_manito[str(student_id % 100)]
        if request.POST:
            manito_account = models.get_manito_account(manito_num)
            manito_account.photo = request.FILES.get('file', None)
            manito_account.save()
            print('saved')

        data['first_manito'] = student_name[str(manito_num)]

    lst = []
    for manito in models.ManitoAccount.objects.all():
        lst.append({
            'name': student_name[str(manito.id)],
            'photo': (lambda: manito.photo.url() if manito.photo.name is None else "")()
        })
    data['manito'] = lst
    print(data)
    return render(request, 'photo.html', data)
