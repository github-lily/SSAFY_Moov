from django.urls import path
from . import views

urlpatterns = [
    # 현재 로그인한 유저 정보 가져오기
    path('', views.get_user),
    # 프로필 페이지
    path('mypage/<int:user_id>/', views.user_profile),
    # 프로필 이미지
    path('upload_img/<int:user_id>/', views.upload_img),


    # path('follow/<username>/', views.follow),
    
]
