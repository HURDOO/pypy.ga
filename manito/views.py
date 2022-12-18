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
    print(lst)
    return render(request, 'about.html', data)
