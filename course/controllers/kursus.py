from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .. import models as db
from website.models import *
from django.http import JsonResponse
from website.decorators import allowed_users
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json
from django.db.models import Q


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def views(request):
    divisions = db.Divisions.objects.order_by('name')
    return render(request, "kursus/list-kursus.html", {'divisions': divisions})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")
    division = request.GET.get("division")

    if request.user.role == 'admin':
        data = db.Courses.objects.order_by("-id")
    elif request.user.role == 'tutor':
        data = db.Courses.objects.filter(division=request.user.division).order_by("-id")

    if division:
        data = data.filter(division__uuid=division)

    if search:
        data = data.filter(title__icontains=search)

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "uuid": obj.uuid,
            "title": obj.title,
            "division": obj.division.name,
            "meetings": obj.meetings.count(),
            "members": obj.members.count()
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
    division = request.POST.get('division')
    title = request.POST.get('title')
    thumbnail = request.FILES.get('thumbnail')

    try:
        course = db.Courses.objects.create(
            title=title,
            division=db.Divisions.objects.get(uuid=division),
            thumbnail=thumbnail
        )
        return JsonResponse({
            'success': 'Kursus berhasil dibuat',
            'uuid': course.uuid
        })
    except:
        return JsonResponse({'error': "Kursus gagal dibuat !"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Courses.objects.filter(uuid=key).delete()
        return JsonResponse({'success': 'Kursus berhasil dihapus'})
    except:
        return JsonResponse({'error': "Kursus gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def edit_views(request, uuid):
    divisions = db.Divisions.objects.order_by('name')
    return render(request, "kursus/edit-kursus.html", {'divisions': divisions})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def get_detail(request, uuid):
    data = db.Courses.objects.get(uuid=uuid)

    meetings = []
    for d in data.meetings.order_by('id'):
        meetings.append({
            'uuid': d.uuid,
            'title': d.title,
            'video': 'https://youtube.com/watch?v=' + d.video if d.video else ''
        })

    members = []
    for m in data.members.order_by('-id'):
        members.append(f"{m.member.first_name} {m.member.last_name}")
    
    row = {
        "title": data.title,
        "division": data.division.uuid,
        "thumbnail": data.thumbnail.url,
        "description": data.description,
        "meetings": meetings,
        "members": members
    }
    
    return JsonResponse(row, safe=False)


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def edit_data(request, uuid):   
    title = request.POST.get('title')
    division = request.POST.get('division')
    description = request.POST.get('description')
    thumbnail = request.FILES.get('thumbnail')

    try:
        course = db.Courses.objects.get(uuid=uuid)
        course.title = title
        course.division = Divisions.objects.get(uuid=division)
        course.description = description
        if thumbnail:
            course.thumbnail = thumbnail
        course.save()

        return JsonResponse({'success': 'Informasi Kursus berhasil diubah'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def add_meeting_views(request, uuid):
    return render(request, "kursus/add-meeting.html", {'course': db.Courses.objects.get(uuid=uuid).title})


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def save_meeting(request, uuid):   
    data = json.loads(request.body) 
    title = data.get('title')
    video = data.get('video')
    material = data.get('material')

    try:
        db.Meetings.objects.create(
            title=title,
            video=video,
            material=material,
            course=db.Courses.objects.get(uuid=uuid)
        )
        return JsonResponse({'success': 'Materi kursus berhasil dibuat',})
    except:
        return JsonResponse({'error': "Materi kursus gagal dibuat !"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def delete_meeting(request, uuid):    
    key = json.loads(request.body).get('key')

    try:
        db.Meetings.objects.filter(uuid=key).delete()
        return JsonResponse({'success': 'Materi kursus berhasil dihapus'})
    except:
        return JsonResponse({'error': "Materi kursus gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def edit_meeting_views(request, uuid, meeting):
    return render(request, "kursus/edit-meeting.html", {'course': db.Courses.objects.get(uuid=uuid).title})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def get_detail_meeting(request, uuid, meeting):
    data = db.Meetings.objects.get(uuid=meeting)
    
    row = {
        "title": data.title,
        "video": data.video,
        "material": data.material,
    }
    
    return JsonResponse(row, safe=False)


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['admin', 'tutor'])
def update_meeting(request, uuid, meeting):   
    data = json.loads(request.body) 
    title = data.get('title')
    video = data.get('video')
    material = data.get('material')

    try:
        meeting = db.Meetings.objects.get(uuid=meeting)
        meeting.title = title
        meeting.video = video
        meeting.material = material
        meeting.save()
        return JsonResponse({'success': 'Materi kursus berhasil diubah',})
    except:
        return JsonResponse({'error': "Materi kursus gagal diubah!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['member'])
def all_courses_views(request):
    divisions = Divisions.objects.order_by('name')
    return render(request, "kursus/list-member-kursus.html", {'divisions': divisions})


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['member'])
def all_courses_get_data(request):
    search = request.GET.get("search")
    division = request.GET.get("division")

    data = db.Courses.objects.order_by("-id")

    if division:
        data = data.filter(division__uuid=division)

    if search:
        data = data.filter(title__icontains=search)

    serialized_data = []
    for obj in data:
        row = {
            "uuid": obj.uuid,
            "title": obj.title,
            "slug": obj.slug,
            "division": obj.division.name,
            "members": obj.members.count(),
            "thumbnail": obj.thumbnail.url,
        }
        serialized_data.append(row)
    
    response_data = {
        'data': serialized_data,
    }
        
    return JsonResponse(json.dumps(response_data), safe=False)


@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['member'])
def detail_course_views(request, slug):
    return render(request, "kursus/detail-member-kursus.html", {
        "course": db.Courses.objects.get(slug=slug),
        "enrolled": True if request.user.enrol.filter(course__slug=slug).exists() else False
    })


@require_POST
@login_required(login_url="/auth/login")
@allowed_users(['member'])
def enrol_course(request, slug):    
    key = json.loads(request.body).get('key')

    try:
        if db.Enrolments.objects.filter(course__slug=slug, member=request.user).exists():
            return JsonResponse({'error': "Kamu sudah daftar kursus ini!"}, status=400)
        else:
            db.Enrolments.objects.create(
                member=request.user,
                course=db.Courses.objects.get(slug=key)
            )
            return JsonResponse({'success': 'Kamu berhasil daftar kursus ini'})
    except:
        return JsonResponse({'error': "Materi kursus gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
@allowed_users(['member'])
def play_course_views(request, slug, meeting):
    enrolled = True if request.user.enrol.filter(course__slug=slug).exists() else False

    if enrolled:
        return render(request, "kursus/play-member-kursus.html", {
            "meeting": db.Meetings.objects.get(uuid=meeting, course__slug=slug),
            "enrolled": enrolled,
            "active": meeting
        })
    else:
        return redirect('kursus_all_course_views')