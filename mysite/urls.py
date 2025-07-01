"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings
# from app.views import IndexView
from app.views import ItemListView # ← ItemListViewを直接インポート
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('python/', include([
        path('admin/', admin.site.urls),
        path('', include('app.urls')),
        path('accounts/', include('allauth.urls')), # もしallauthを使っている場合
    

    # パスワードリセット要求ページ
    path('accounts/password/reset/', 
        auth_views.PasswordResetView.as_view(
            # あなたのファイル名に合わせます
            template_name="registration/password_reset.html" 
        ), 
        name='password_reset'),

    # メール送信完了ページ
    path('accounts/password/reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            # あなたのファイル名に合わせます
            template_name="registration/password_reset_mail_done.html"
        ), 
        name='password_reset_done'),

    # 新パスワード入力ページ
    path('accounts/password/reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            # あなたのファイル名に合わせます
            template_name="registration/password_reset_confirmation.html"
        ), 
        name='password_reset_confirm'),

    # パスワードリセット完了ページ
    path('accounts/password/reset/complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            # あなたのファイル名に合わせます
            template_name="registration/password_reset_finish.html"
        ), 
        name='password_reset_complete'),

    # --- パスワード変更関連も同様に設定可能 ---
    path('accounts/password/change/',
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html"
        ),
        name='password_change'),
    
    path('accounts/password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_finish.html"
        ),
        name='password_change_done'),


    path('', include('app.urls')),
    path('', ItemListView.as_view(), name='index'), 

    
     # --- 認証関連 ---
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    
    # --- 決済キャンセルページ ---
    path('cancel/', TemplateView.as_view(template_name="payment/cancel.html"), name="payment_cancel"),
    ]))
    
]

# 開発環境でのみメディアファイルと静的ファイルを配信するための設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)