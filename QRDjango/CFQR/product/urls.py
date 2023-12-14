from django.urls import path, re_path
from . import views

urlpatterns = [
    path('upload', views.product_image, name='upload'),
    re_path('qrlist/.*', views.qr_list, name='qrlist'),
    path('migrate', views.migrate, name='migrate'),
    re_path(r'^.*', views.product_qr, name='product'),
]