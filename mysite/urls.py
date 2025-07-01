# mysite/urls.py (最終完成形)

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 管理サイト
    path('admin/', admin.site.urls),
    
    # 認証関連 (allauth)
    path('accounts/', include('allauth.urls')),
    
    # カスタムアカウントページ
    path('accounts/', include('accounts.urls')),
    
    # 決済キャンセルページ
    path('cancel/', TemplateView.as_view(template_name="payment/cancel.html"), name="payment_cancel"),
    
    # メインのアプリケーション
    path('', include('app.urls')),
]

# 開発環境用の設定 (本番環境では影響しません)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)