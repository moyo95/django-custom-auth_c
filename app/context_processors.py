# app/context_processors.py (新規作成)

from .models import Order

def cart(request):
    """
    サイトのどのページからでも、テンプレートで {{ cart }} と書くだけで、
    ログイン中のユーザーのカート情報（未注文のものだけ）を呼び出せるようにする。
    """
    if request.user.is_authenticated:
        # getではなくfilterを使うことで、カートがなくてもエラーにならない
        # first()で、最初の一つを取得するか、なければNoneを返す
        order = Order.objects.filter(user=request.user, ordered=False).first()
        if order:
            return {'cart': order}
    # ユーザーがログインしていない場合や、カートがない場合はNoneを返す
    return {'cart': None}