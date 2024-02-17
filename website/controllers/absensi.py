from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json, locale
from django.db.models import Q

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def views(request):
    divisions = db.Divisions.objects.order_by('name')
    return render(request, "absensi/list-absensi.html", {'divisions': divisions})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def get_data(request):
    page = request.GET.get("page")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    division = request.GET.get("division")

    if request.user.role == 'admin':
        data = db.Presences.objects.order_by("-id")
    elif request.user.role == 'tutor':
        data = db.Presences.objects.filter(division=request.user.division).order_by("-id")

    if division:
        data = data.filter(division__uuid=division)

    if start_date and end_date:
        data = data.filter(date__range=[start_date, end_date])

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "uuid": obj.uuid,
            "date": obj.date.strftime('%A, %d %b %Y') if obj.date else '-',
            "division": obj.division.name,
            "present": obj.detail.count()
        }
        serialized_data.append(row)
            
    pagination_info = {
        'has_next': current_page.has_next(),
        'has_previous': current_page.has_previous(),
        'current_page_number': current_page.number,
        'total_page': paginator.num_pages,
        'total_data': data.count()
    }
    
    response_data = {
        'data': serialized_data,
        'pagination': pagination_info
    }
        
    return JsonResponse(json.dumps(response_data), safe=False)


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def add_data(request):    
    data = json.loads(request.body)
    division = data.get('division')
    note = data.get('note')

    try:
        if request.user.role == 'admin':
            presence = db.Presences.objects.create(
                note=note,
                division=db.Divisions.objects.get(uuid=division)
            )
        elif request.user.role == 'tutor':
            presence = db.Presences.objects.create(
                note=note,
                division=request.user.division
            )
        return JsonResponse({
            'success': 'Data absensi berhasil dibuat',
            'uuid': presence.uuid
        })
    except:
        return JsonResponse({'error': "Data absensi gagal dibuat !"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Presences.objects.filter(uuid=key).delete()
        return JsonResponse({'success': 'Data absensi berhasil dihapus'})
    except:
        return JsonResponse({'error': "Data absensi gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def edit_views(request, uuid):
    return render(request, "absensi/edit-absensi.html")


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def get_detail(request, uuid):
    data = db.Presences.objects.get(uuid=uuid)
    detail = db.DetailPresence.objects.filter(presence=data)

    details = []
    for d in detail:
        details.append({
            'id': d.id,
            'name': f'{d.member.first_name} {d.member.last_name}',
            'npm': d.member.username,
            'datetime': d.datetime.strftime('%d-%m-%Y, %H:%M')
        })
    
    row = {
        "division": data.division.name,
        "tutor": f'{data.division.tutor.first_name} {data.division.tutor.last_name}',
        "date": data.date.strftime('%A, %d %b %Y'),
        "note": data.note,
        "qrcode": data.qrcode.url,
        "details": details
    }
    
    return JsonResponse(row)