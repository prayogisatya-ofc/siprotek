from django.shortcuts import render, redirect
from .. import models as db
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
import json, random
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required


def create_captcha(request):
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    correct_answer = num1 + num2
    request.session['correct_answer'] = correct_answer
    return {'num1': num1, 'num2': num2}


@require_GET
def views(request):
    if request.user.is_authenticated:
        return redirect('dashboard_views')
    else:
        return render(request, "auth/login.html", context=create_captcha(request))


@require_POST
def auth(request):
    data = json.loads(request.body)
    
    npm = data.get("npm")
    password = data.get("password")
    captcha = int(data.get('captcha'))
    correct_answer = request.session.get('correct_answer', 0)
    
    if captcha == correct_answer:
        user = db.User.objects.filter(username=npm, is_active=True)
        if user.exists():
            cek_pass = check_password(password, user[0].password)
            if cek_pass:
                login(request, user[0])
                return JsonResponse({'success': 'Yeyy kamu berhasil masuk'})
        return JsonResponse({'error': 'NPM atau Password ada yang salah!'}, status=400)
    else:
        return JsonResponse({'error': 'Yahh captcha salah!'}, status=400)
    

@require_GET
@login_required(login_url='/auth/login')
def logouts(request):
    logout(request)
    return redirect("login_views")