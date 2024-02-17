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
    return render(request, "prodi/list-prodi.html")


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")

    data = db.Majors.objects.order_by("name")

    if search:
        data = data.filter(name__icontains=search)

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "uuid": obj.uuid,
            "name": obj.name,
            "code": obj.code,
            "members": obj.users.all().count()
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
    return render(request, "prodi/add-prodi.html")


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def add_data(request):    
    datas = json.loads(request.body)

    try:
        for data in datas:
            if data.get('name') != '' and data.get('code') != '':
                db.Majors.objects.create(name=data.get('name'), code=data.get('code'))
        return JsonResponse({'success': 'Data prodi berhasil disimpan'})
    except:
        return JsonResponse({'error': "Data prodi gagal disimpan!"}, status=400)


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Majors.objects.filter(uuid=key).delete()
        return JsonResponse({'success': 'Data prodi berhasil dihapus'})
    except:
        return JsonResponse({'error': "Data prodi gagal dihapus!"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def edit_data(request):
    data = json.loads(request.body)
    uuid = data.get('uuid')
    name = data.get('name')
    code = data.get('code')

    try:
        data = db.Majors.objects.get(uuid=uuid)
        data.name = name
        data.code = code
        data.save()
        
        return JsonResponse({'success': 'Data prodi berhasil diupdate'})
    except:
        return JsonResponse({'error': "Data prodi gagal diupdate!"}, status=400)