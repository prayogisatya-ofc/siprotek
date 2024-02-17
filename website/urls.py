from django.urls import path
from .controllers import (
    auth, dashboard, anggota, 
    prodi, admin, tutor, divisi, 
    absensi, scanqr, akun
)

urlpatterns = [
    path('auth/login', auth.views, name='login_views'),
    path('auth/login/authenticate', auth.auth, name='login_authenticate'),
    path('auth/logout', auth.logouts, name='logout'),

    path('', dashboard.views, name='dashboard_views'),

    path('members', anggota.views, name='members_views'),
    path('members/get-data', anggota.get_data, name='members_get_data'),
    path('members/add', anggota.add_views, name='members_add_views'),
    path('members/add/submit', anggota.add_data, name='members_add_data'),
    path('members/delete', anggota.delete_data, name='members_delete_data'),
    path('members/import', anggota.import_file, name='members_import_file'),
    path('members/<str:uuid>', anggota.edit_views, name='members_edit_views'),
    path('members/<str:uuid>/get-data', anggota.get_detail, name='members_edit_get_detail'),
    path('members/<str:uuid>/submit', anggota.edit_data, name='members_edit_data'),

    path('majors', prodi.views, name='majors_views'),
    path('majors/get-data', prodi.get_data, name='majors_get_data'),
    path('majors/add', prodi.add_views, name='majors_add_views'),
    path('majors/add/submit', prodi.add_data, name='majors_add_data'),
    path('majors/delete', prodi.delete_data, name='majors_delete_data'),
    path('majors/update', prodi.edit_data, name='majors_edit_data'),

    path('admins', admin.views, name='admin_views'),
    path('admins/get-data', admin.get_data, name='admin_get_data'),
    path('admins/add', admin.add_views, name='admin_add_views'),
    path('admins/add/submit', admin.add_data, name='admin_add_data'),
    path('admins/delete', admin.delete_data, name='admin_delete_data'),
    path('admins/<str:uuid>', admin.edit_views, name='admin_edit_views'),
    path('admins/<str:uuid>/get-data', admin.get_detail, name='admin_edit_get_detail'),
    path('admins/<str:uuid>/submit', admin.edit_data, name='admin_edit_data'),

    path('tutors', tutor.views, name='tutor_views'),
    path('tutors/get-data', tutor.get_data, name='tutor_get_data'),
    path('tutors/add', tutor.add_views, name='tutor_add_views'),
    path('tutors/add/submit', tutor.add_data, name='tutor_add_data'),
    path('tutors/delete', tutor.delete_data, name='tutor_delete_data'),
    path('tutors/<str:uuid>', tutor.edit_views, name='tutor_edit_views'),
    path('tutors/<str:uuid>/get-data', tutor.get_detail, name='tutor_edit_get_detail'),
    path('tutors/<str:uuid>/submit', tutor.edit_data, name='tutor_edit_data'),

    path('divisions', divisi.views, name='divisi_views'),
    path('divisions/get-data', divisi.get_data, name='divisi_get_data'),
    path('divisions/add', divisi.add_views, name='divisi_add_views'),
    path('divisions/add/submit', divisi.add_data, name='divisi_add_data'),
    path('divisions/delete', divisi.delete_data, name='divisi_delete_data'),
    path('divisions/update', divisi.edit_data, name='divisi_edit_data'),

    path('presences', absensi.views, name='absensi_views'),
    path('presences/get-data', absensi.get_data, name='absensi_get_data'),
    path('presences/add', absensi.add_data, name='absensi_add_data'),
    path('presences/delete', absensi.delete_data, name='absensi_delete_data'),
    path('presences/<str:uuid>', absensi.edit_views, name='absensi_edit_views'),
    path('presences/<str:uuid>/get-data', absensi.get_detail, name='absensi_edit_get_detail'),

    path('scanqr', scanqr.views, name='scanqr_views'),
    path('scanqr/submit', scanqr.absensi, name='scanqr_absensi'),

    path('account', akun.views, name='akun_views'),
    path('account/get-data', akun.get_detail, name='akun_get_data'),
    path('account/submit', akun.edit_data, name='akun_edit_data'),
    path('password', akun.password_views, name='password_views'),
    path('password/submit', akun.edit_password, name='password_edit'),

]