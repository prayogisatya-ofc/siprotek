from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users
from django.views.decorators.http import require_GET, require_POST
import json, phonenumbers
from django.contrib.auth.hashers import make_password, check_password


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['member', 'tutor'])
def views(request):
    majors = db.Majors.objects.order_by('name')
    return render(request, "akun/akun.html", {'majors': majors})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['tutor', 'member'])
def get_detail(request):
    data = db.User.objects.get(uuid=request.user.uuid)
    
    row = {
        "first_name": data.first_name,
        "last_name": data.last_name,
        "npm": data.username,
        "telp": data.telp,
        "major": data.major.uuid
    }
    
    return JsonResponse(row)


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['member', 'tutor'])
def edit_data(request):   
    data = json.loads(request.body) 
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    telp = data.get('telp')
    major = data.get('major')

    try:
        telp_parse = phonenumbers.parse(telp, "ID")
        telp_format = phonenumbers.format_number(telp_parse, phonenumbers.PhoneNumberFormat.E164)
        telp_result = telp_format.replace("+", "")

        user = db.User.objects.get(uuid=request.user.uuid)
        user.first_name = first_name
        user.last_name = last_name
        user.telp = telp_result
        user.major = db.Majors.objects.get(uuid=major)
        user.save()

        return JsonResponse({'success': 'Detail akun berhasil diubah'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['member', 'tutor'])
def password_views(request):
    return render(request, "akun/password.html")


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['member', 'tutor'])
def edit_password(request):   
    data = json.loads(request.body) 
    current_pw = data.get('current_pw')
    new_pw = data.get('new_pw')
    confirm_pw = data.get('confirm_pw')

    try:
        user = db.User.objects.get(uuid=request.user.uuid)
        if check_password(current_pw, user.password):
            if new_pw == confirm_pw:
                user.password = make_password(new_pw, hasher="pbkdf2_sha256")
                user.save()
                return JsonResponse({'success': 'Password berhasil diubah'})
            return JsonResponse({'error': 'Password Baru dan Konfirmasi Password tidak sama!'}, status=400)
        return JsonResponse({'error': 'Password Sekarang salah!'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)