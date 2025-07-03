# app/tasks.py
from celery import shared_task
from django.core.mail import get_connection, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email_task(order_id):
    """注文完了メールを非同期で送信するタスク（手動接続版）"""
    try:
        order = Order.objects.get(id=order_id)
        order.user.refresh_from_db()

        # settings.pyから接続設定を取得して接続を確立
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            
            # --- ユーザー向けメールの作成と送信 ---
            user_subject = render_to_string('app/email/order_confirmation_subject.txt', {'order': order}).strip()
            user_body = render_to_string('app/email/order_confirmation_body.txt', {'order': order})
            
            user_email = EmailMessage(
                user_subject,
                user_body,
                settings.DEFAULT_FROM_EMAIL,
                [order.user.email], # 送信先
                connection=connection # この接続を使う
            )
            user_email.send()
            print(f"ユーザー向けメールを送信しました (Order ID: {order_id})")
            
            # --- 管理者向けメールの作成と送信 ---
            admin_subject = f"【新規注文】注文がありました (注文番号: {order.id})"
            admin_body = render_to_string('app/email/admin_notification_body.txt', {'order': order})
            
            # settings.ADMINSから宛先リストを作成
            admin_recipients = [admin[1] for admin in settings.ADMINS]
            if admin_recipients:
                admin_email = EmailMessage(
                    admin_subject,
                    admin_body,
                    settings.DEFAULT_FROM_EMAIL,
                    admin_recipients, # 管理者リストに送信
                    connection=connection # 同じ接続を再利用
                )
                admin_email.send()
                print(f"管理者向け通知メールを送信しました (Order ID: {order_id})")

        return f"Successfully sent emails for order {order_id} using manual connection."

    except Order.DoesNotExist:
        return f"Error: Order with id={order_id} not found."
    except Exception as e:
        print(f"タスク内でエラー発生: {e}")
        # Celeryのリトライ機能に任せるため、例外を再発生させる
        raise e