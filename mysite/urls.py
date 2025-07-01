# mysite/urls.py (あなたのコードを元にした最終完成形)

"""
このURL設定は、プロジェクト全体のURLを管理します。
Nginxによって `/python/` が取り除かれた後のパスが、ここで処理されます。
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. 管理サイト (例: /admin/)
    path('admin/', admin.site.urls),

    # 2. 認証関連 (django-allauthが全てを担当)
    #    ログイン、ログアウト、サインアップ、パスワードリセット、パスワード変更など、
    #    あなたが手動で設定していた機能は、すべてこの一行に含まれています。
    path('accounts/', include('allauth.urls')),

    # 3. あなたが作成したカスタムアカウントページ (例: プロフィールページ)
    #    allauthの後に読み込むことで、allauthにないURLだけがここで処理されます。
    path('accounts/', include('accounts.urls')),
    
    # 4. 決済キャンセルページ (例: /cancel/)
    path('cancel/', TemplateView.as_view(template_name="payment/cancel.html"), name="payment_cancel"),

    # 5. メインのアプリケーション (商品一覧、詳細ページなど)
    #    これが最後にくることで、他の具体的なURLにマッチしなかった場合に処理されます。
    #    あなたの `path('', ItemListView.as_view())` の機能は、
    #    この `app.urls` の中で定義するのが正しい方法です。
    path('', include('app.urls')),
]

# 開発環境 (DEBUG=True) のでのみ、メディアファイルと静的ファイルを配信するための設定です。
# 本番環境 (DEBUG=False) では、Nginxがこれらのファイルを配信するため、この部分は影響しません。
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)