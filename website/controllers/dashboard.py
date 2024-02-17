from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users

@login_required(login_url="/auth/login")
@allowed_users(['admin', 'member', 'tutor'])
def views(request):
    members = db.User.objects.filter(role='member', is_active=True).count()
    tutors = db.User.objects.filter(role='tutor').count()
    divisions = db.Divisions.objects.count()
    majors = db.Majors.objects.count()

    context = {
        'members': members,
        'divisions': divisions,
        'majors': majors,
        'tutors': tutors,
    }

    if request.user.role == 'admin':
        return render(request, "dashboard.admin.html", context)
    elif request.user.role == 'tutor':
        return render(request, "dashboard.tutor.html", context)
    else:
        return render(request, "dashboard.member.html", context)