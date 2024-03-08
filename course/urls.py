from django.urls import path
from .controllers import (
    kursus
)

urlpatterns = [
    path('courses', kursus.views, name='kursus_views'),
    path('courses/get-data', kursus.get_data, name='kursus_get_data'),
    path('courses/delete', kursus.delete_data, name='kursus_delete_data'),
    path('courses/add', kursus.add_data, name='kursus_add_data'),
    path('courses/<str:uuid>', kursus.edit_views, name='kursus_edit_views'),
    path('courses/<str:uuid>/get-data', kursus.get_detail, name='kursus_edit_get_data'),
    path('courses/<str:uuid>/update', kursus.edit_data, name='kursus_edit_update_data'),
    path('courses/<str:uuid>/add', kursus.add_meeting_views, name='kursus_add_meeting_views'),
    path('courses/<str:uuid>/add/submit', kursus.save_meeting, name='kursus_save_meeting'),
    path('courses/<str:uuid>/delete', kursus.delete_meeting, name='kursus_delete_meeting'),
    path('courses/<str:uuid>/<str:meeting>', kursus.edit_meeting_views, name='kursus_edit_meeting_views'),
    path('courses/<str:uuid>/<str:meeting>/get-data', kursus.get_detail_meeting, name='kursus_get_detail_meeting'),
    path('courses/<str:uuid>/<str:meeting>/submit', kursus.update_meeting, name='kursus_update_meeting'),

    path('all-courses', kursus.all_courses_views, name='kursus_all_course_views'),
    path('all-courses/get-data', kursus.all_courses_get_data, name='kursus_all_course_get_daya'),
    path('all-courses/<str:slug>', kursus.detail_course_views, name='kursus_detail_course_views'),
    path('all-courses/<str:slug>/enrol', kursus.enrol_course, name='kursus_enrol_course'),
    path('all-courses/<str:slug>/<str:meeting>', kursus.play_course_views, name='kursus_play_course'),
]