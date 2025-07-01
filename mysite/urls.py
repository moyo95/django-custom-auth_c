# mysite/urls.py (最終診断用)

from django.http import HttpResponse

# ★★★ ここに直接、世界一簡単なビューを書く ★★★
def test_view(request):
    return HttpResponse("Hello, Django is working!")

urlpatterns = [
    # ★★★ トップページへのアクセスは、必ずこのビューが応答する ★★★
    path('', test_view),
]