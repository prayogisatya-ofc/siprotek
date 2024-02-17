from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json, phonenumbers
from django.db.models import Q
from django.contrib.auth.hashers import make_password


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def views(request):
    return render(request, "tutor/list-tutor.html")


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")

    data = db.User.objects.filter(role="tutor").order_by("first_name")

    if search:
        data = data.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "uuid": obj.uuid,
            "name": f"{obj.first_name} {obj.last_name}",
            "npm": obj.username,
            "major": obj.major.name,
            "telp": obj.telp,
            "is_active": obj.is_active
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
    majors = db.Majors.objects.all()
    return render(request, "tutor/add-tutor.html", {'majors': majors})


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def add_data(request):    
    data = json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    telp = data.get('telp')
    major = data.get('major')
    npm = data.get('npm')
    password = data.get('password')

    try:
        telp_parse = phonenumbers.parse(telp, "ID")
        telp_format = phonenumbers.format_number(telp_parse, phonenumbers.PhoneNumberFormat.E164)
        telp_result = telp_format.replace("+", "")

        db.User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=npm,
            password=password,
            major=db.Majors.objects.get(uuid=major),
            telp=telp_result,
            role='tutor'
        )
        return JsonResponse({'success': 'Data tutor berhasil disimpan'})
    except:
        return JsonResponse({'error': "Data tutor gagal disimpan!"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.User.objects.filter(uuid=key).delete()
        return JsonResponse({'success': 'Data tutor berhasil dihapus'})
    except:
        return JsonResponse({'error': "Data tutor gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def edit_views(request, uuid):
    majors = db.Majors.objects.all()
    return render(request, "tutor/edit-tutor.html", {'majors': majors})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def get_detail(request, uuid):
    data = db.User.objects.get(uuid=uuid)
    
    row = {
        "uuid": data.uuid,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "npm": data.username,
        "telp": data.telp,
        "major": data.major.uuid,
        "status": data.is_active
    }
    
    return JsonResponse(row)


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def edit_data(request, uuid):   
    data = json.loads(request.body) 
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    telp = data.get('telp')
    major = data.get('major')
    npm = data.get('npm')
    password = data.get('password')
    status = str(data.get('status'))

    try:
        telp_parse = phonenumbers.parse(telp, "ID")
        telp_format = phonenumbers.format_number(telp_parse, phonenumbers.PhoneNumberFormat.E164)
        telp_result = telp_format.replace("+", "")

        user = db.User.objects.get(uuid=uuid)
        user.first_name = first_name
        user.last_name = last_name
        user.telp = telp_result
        user.major = db.Majors.objects.get(uuid=major)
        user.username = npm
        user.is_active = status.lower() == "true"
        if password:
            user.password = make_password(password, hasher="pbkdf2_sha256")
        user.save()

        return JsonResponse({'success': 'Data tutor berhasil diubah'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)