from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users
from django.views.decorators.http import require_GET, require_POST
import json


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['member'])
def views(request):
    return render(request, "scanqr.html")


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['member'])
def absensi(request):    
    data = json.loads(request.body)
    kode = data.get('kode')

    try:
        presence = db.Presences.objects.filter(uuid=kode)
        if presence.exists():
            if not db.DetailPresence.objects.filter(presence=presence.first(), member=request.user).exists():
                db.DetailPresence.objects.create(
                    presence=presence.first(),
                    member=request.user
                )
                return JsonResponse({'success': 'Yeyy.. Kamu berhasil absen'})
            else:
                return JsonResponse({'error': "Kamu udah absen yaa!"}, status=400)
        else:
            return JsonResponse({'error': "Tidak absensi dengan kode ini!"}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)