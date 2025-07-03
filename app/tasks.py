# app/tasks.py
from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email_task(order_id):
    """注文完了メールを非同期で送信するタスク"""
    try:
        order = Order.objects.get(id=order_id)

        order.user.refresh_from_db()

        subject = render_to_string('app/email/order_confirmation_subject.txt', {'order': order}).strip()
        # ▼▼▼ ここを修正 ▼▼▼
        context = {
            'order': order,
            'user': order.user  # 'user' をコンテキストに追加
        }
        body = render_to_string('app/email/order_confirmation_body.txt', context)
        # ▲▲▲ 修正ここまで ▲▲▲
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=False,
        )

        print(f"ユーザー向けメールを送信しました (Order ID: {order_id})")

        # --- 2. 管理者向け通知メールの送信（追加する処理） ---
        admin_subject = f"【新規注文】注文がありました (注文番号: {order.id})"
        # 管理者向けに、より詳細なテンプレートを用意すると親切
        admin_body = render_to_string('app/email/admin_notification_body.txt', {'order': order})

        # settings.py の ADMINS に設定されたメールアドレスに一斉送信する
        mail_admins(
            admin_subject,
            admin_body,
            fail_silently=False,
        )
        print(f"管理者向け通知メールを送信しました (Order ID: {order_id})")
        

        return f"Successfully sent email for order {order_id}"

    except Order.DoesNotExist:
        return f"Error: Order with id={order_id} not found."
    except Exception as e:
        # Celeryのリトライ機能に任せるため、例外を再発生させる
        raise e