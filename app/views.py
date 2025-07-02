from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Item, OrderItem, Order, Payment
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
import stripe
from django.conf import settings
from django.http import JsonResponse
import traceback
from django.views.generic import TemplateView
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Item
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Order


# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin


# class IndexView(LoginRequiredMixin,TemplateView):
#     template_name = 'app/index.html'


class IndexView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.all()
        return render(request, 'app/index.html', {
            'item_data': item_data
        })
    
class ItemDetailView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs['slug'])
        return render(request, 'app/product.html', {
            # 'item_data': item_data
            'object': item_data,
        })
    

@login_required
def addItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity  += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order =Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)

    return redirect('app:order')

class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order
            }
            return render(request, 'app/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/order.html')
        

@login_required
def removeItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect('app:order')
        
    return redirect('app:product', slug=slug)

@login_required
def removeSingleItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect('app:order')
    return redirect('app:product', slug=slug)

class PaymentView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
         order = Order.objects.get(user=request.user, ordered=False)
         user_data = CustomUser.objects.get(id=request.user.id)
         context = {
             'order': order,
             'user_data': user_data,
             'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY  # ← 追加
         }
         return render(request, 'app/payment.html', context)
     
     def post(self, request, *args, **kwargs):
         stripe.api_key = settings.STRIPE_SECRET_KEY
         order = Order.objects.get(user=request.user, ordered=False)
         token = request.POST.get('stripeToken')
         order_items = order.items.all()
         amount = order.get_total()
         item_list = []
         for order_item in order_items:
             item_list.append(str(order_item.item) + ':' + str(order_item.quantity))
         description = ' '.join(item_list)

         charge = stripe.Charge.create(
             amount=amount,
             currency='jpy',
             description=description,
            #  payment_method="pm_card_visa",
             source=token
         )

         payment = Payment(user=request.user)
         payment.stripe_change_id = charge['id']
         payment.amount = amount
         payment.save()

         order_items.update(ordered=True)
         for item in order_items:
             item.save()

         order.ordered = True
         order.payment = payment
         order.save()
         return redirect('thanks')

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            
            line_items = []
            for item in order_items:
                line_items.append({
                    'price_data': {
                        'currency': 'jpy',
                        'product_data': {
                            'name': item.item.title,
                        },
                        'unit_amount': int(item.item.price),
                    },
                    'quantity': item.quantity,
                })

            protocol = 'https' if request.is_secure() else 'http'
            host = request.get_host()

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                # success_url='http://localhost:8000/success/',
                # cancel_url='http://localhost:8000/cancel/',
                client_reference_id=order.id, 
                success_url=f"{protocol}://{host}{reverse('app:thanks')}",
                cancel_url=f"{protocol}://{host}{reverse('payment_cancel')}",
            )
            return JsonResponse({'id': session.id})
        
        except Exception as e:
            print(traceback.format_exc())
            logger.error("Error creating Stripe Checkout Session: %s", e)
            return JsonResponse({'error': str(e)}, status=500)

class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/thanks.html')

class PaymentCancelView(TemplateView):
    template_name = 'payment/cancel.html'

class ItemListView(ListView):
    model = Item
    template_name = 'app/item_list.html'
    context_object_name = 'item_data'  # ここでテンプレートに渡す変数名を指定
    paginate_by = 8

#     queryset = Item.objects.all().order_by('-created_at') # created_atはモデルの作成日時フィールド名

#     def get_queryset(self):
#         category = self.request.GET.get('category')
#         if category:
#             return Item.objects.filter(category=category)
#         return Item.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # カテゴリ一覧をItemから重複なしで抽出
#         context['categories'] = Item.objects.values_list('category', flat=True).distinct()
#         return context

# def some_view(request):
#     user_data = request.user  # または User.objects.get(...)
#     return render(request, 'template.html', {'user_data': user_data})
    def get_queryset(self):
        # 'created_at' を 'id' に変更
        queryset = super().get_queryset().order_by('-id')

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Item.objects.values_list('category', flat=True).distinct()
        return context



def signup_view(request):
    # ... ユーザー登録とメール送信処理 ...
    context = {
        'status': 'signup_success' # 新規登録成功のステータス
    }
    return render(request, 'app/confirm-email.html', context)

# 例2: 確認メール再送のビュー
def resend_confirmation_email_view(request):
    # ... メール再送処理 ...
    context = {
        'status': 'resend_success' # 再送成功のステータス
    }
    return render(request, 'app/confirm-email.html', context)

# 例3: メール認証リンククリック時のビュー
def activate_view(request, uidb64, token):
    # ... ユーザー認証処理 ...
    if user_is_already_active:
        context = {
            'status': 'already_verified' # 認証済みのステータス
        }
        return render(request, 'app/confirm-email.html', context)
    # ... 認証成功・失敗の処理 ...



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET # .envから読み込む
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return HttpResponse(status=400)

    # checkout.session.completed イベントを処理
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # ★★★ ここが「商品を袋に入れる」処理 ★★★
        try:
            # sessionから、あなたのサイトの注文IDなどを取得する方法が必要です
            # ここでは例として、client_reference_idを使います
            order_id = session.client_reference_id
            if order_id:
                order = Order.objects.get(id=order_id)
                order.ordered = True # 注文済みにする
                order.save()
                print(f"注文ID: {order.id} が支払い済みに更新されました。")

                # ★★★ ここからがメール送信処理 ★★★
                subject = render_to_string('app/email/order_confirmation_subject.txt', {
                    'order': order,
                }).strip()
                
                body = render_to_string('app/email/order_confirmation_body.txt', {
                    'order': order,
                    'user': order.user,
                })

                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL, # 送信元 (.envで設定)
                    [order.user.email],         # 送信先
                    fail_silently=False,
                )
                print(f"注文ID: {order.id} の注文完了メールを送信しました。")
                # ★★★ メール送信処理はここまで ★★★
                
                # ★★★ ここが重要：新しい空のカートを作成する ★★★
                new_order = Order.objects.create(user=order.user, ordered=False)
                print(f"ユーザー {order.user} のために新しいカート {new_order.id} を作成しました。")
            else:
                print("Webhookでclient_reference_idが見つかりませんでした。")

        except Order.DoesNotExist:
            print(f"Webhookエラー: 注文ID {order_id} が見つかりません。")
            return HttpResponse(status=404)
        except Exception as e:
            print(f"Webhook処理エラー: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)