from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def views(request):
    tutors = db.User.objects.filter(role='tutor')
    return render(request, "divisi/list-divisi.html", {'tutors': tutors})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")

    data = db.Divisions.objects.order_by("name")

    if search:
        data = data.filter(name__icontains=search)

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "uuid": obj.uuid,
            "name": obj.name,
            "tutor": f'{obj.tutor.first_name} {obj.tutor.last_name}',
            "tutor_uuid": obj.tutor.uuid
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


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def add_views(request):
    tutors = db.User.objects.filter(role='tutor')
    return render(request, "divisi/add-divisi.html", {'tutors': tutors})


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def add_data(request):    
    datas = json.loads(request.body)

    try:
        for data in datas:
            if data.get('name') != '' and data.get('tutor') != '':
                db.Divisions.objects.create(
                    name=data.get('name'), 
                    tutor=db.User.objects.get(uuid=data.get('tutor'))
                )
        return JsonResponse({'success': 'Data divisi berhasil disimpan'})
    except:
        return JsonResponse({'error': "Data divisi gagal disimpan!"}, status=400)


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Divisions.objects.filter(uuid=key).delete()
        return JsonResponse({'success': 'Data divisi berhasil dihapus'})
    except:
        return JsonResponse({'error': "Data divisi gagal dihapus!"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def edit_data(request):
    data = json.loads(request.body)
    uuid = data.get('uuid')
    name = data.get('name')
    tutor = data.get('tutor_uuid')

    try:
        data = db.Divisions.objects.get(uuid=uuid)
        data.name = name
        data.tutor = db.User.objects.get(uuid=tutor)
        data.save()
        
        return JsonResponse({'success': 'Data divisi berhasil diupdate'})
    except:
        return JsonResponse({'error': "Data divisi gagal diupdate!"}, status=400)