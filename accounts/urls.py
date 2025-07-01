# urls.py

from django.urls import path, include
from accounts import views  # ProfileViewなど自作ビューのために必要
from app.views import IndexView

app_name = 'accounts' 

urlpatterns = [
    # ===================================================================
    # 1. allauthのURLをインクルードする (これだけで認証機能はほぼ揃う)
    # ===================================================================
    path('accounts/', include('allauth.urls')),


    # ===================================================================
    # 2. あなたが独自に作成したページのURL (allauthと衝突しないもの)
    # ===================================================================
    path('', IndexView.as_view(), name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    


    # ===================================================================
    # 3. 注意：パスワードリセット機能について
    # allauthにもパスワードリセット機能は含まれています。
    # ('/accounts/password/reset/')
    # もしDjango標準の機能を使いたい場合は、このまま残しても構いませんが、
    # allauthのデザインと統一したい場合は、allauthの機能を使うことを推奨します。
    # 一旦、このまま残しておきます。
    # ===================================================================
    # from django.contrib.auth import views as auth_views
    # path('password_reset_form/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html', from_email=' office54@office54.net '), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_mail_done.html'), name='password_reset_done'),
    # path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirmation.html'), name='password_reset_confirm'),
    # path('password_reset_finish/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_finish.html'), name='password_reset_complete'),
    # path('accounts/password_change_form/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change_form'),
    # path('accounts/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_finish.html'), name='password_change_done'),
]