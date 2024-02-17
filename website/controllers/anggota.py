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
from django.db import transaction
import pandas as pd


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def views(request):
    majors = db.Majors.objects.order_by('name')
    return render(request, "anggota/list-anggota.html", {'majors': majors})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")
    major = request.GET.get("major")
    status = str(request.GET.get("status"))

    data = db.User.objects.filter(role="member").order_by("username")

    if search:
        data = data.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    if major:
        data = data.filter(major__uuid=major)

    if status:
        data = data.filter(is_active=status.lower() == "true")

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
    return render(request, "anggota/add-anggota.html", {'majors': majors})


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
            role='member'
        )
        return JsonResponse({'success': 'Data anggota berhasil disimpan'})
    except:
        return JsonResponse({'error': "Data anggota gagal disimpan!"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.User.objects.filter(uuid=key).delete()
        return JsonResponse({'success': 'Data anggota berhasil dihapus'})
    except:
        return JsonResponse({'error': "Data anggota gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def edit_views(request, uuid):
    majors = db.Majors.objects.all()
    return render(request, "anggota/edit-anggota.html", {'majors': majors})


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

        member = db.User.objects.get(uuid=uuid)
        member.first_name = first_name
        member.last_name = last_name
        member.telp = telp_result
        member.major = db.Majors.objects.get(uuid=major)
        member.username = npm
        member.is_active = status.lower() == "true"
        if password:
            member.password = make_password(password, hasher="pbkdf2_sha256")
        member.save()

        return JsonResponse({'success': 'Data anggota berhasil diubah'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin'])
def import_file(request):
    file = request.FILES['file']

    try:
        with transaction.atomic():
            df = pd.read_excel(file, engine='openpyxl')

            columns = df.columns

            required_columns = ['NPM', 'Nama Depan', 'Nama Belakang', 'Kode Prodi', 'No. Telepon']
            if not all(column in columns for column in required_columns):
                return JsonResponse({'error': 'Kolom yang diperlukan tidak ditemukan'}, status=400)

            for index, row in df.iterrows():
                if not db.User.objects.filter(username=row['NPM']).exists():
                    try:
                        telp_parse = phonenumbers.parse(str(row['No. Telepon']), "ID")
                        telp_format = phonenumbers.format_number(telp_parse, phonenumbers.PhoneNumberFormat.E164)
                        telp_result = telp_format.replace("+", "")

                        db.User.objects.create_user(
                            username=str(row['NPM']),
                            first_name=row['Nama Depan'],
                            last_name=row['Nama Belakang'],
                            password=str(row['NPM']),
                            major=db.Majors.objects.get(code=row['Kode Prodi']),
                            telp=telp_result,
                            role='member'
                        )
                    except Exception as e:
                        return JsonResponse({'error': f'Error pada baris {index + 2}: {str(e)}'}, status=400)

            return JsonResponse({'success': 'Data siswa berhasil diimpor'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)