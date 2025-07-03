# app/tasks.py
from celery import shared_task
from django.core.mail import get_connection, EmailMessage # インポートを変更
from django.conf import settings
from .models import Order # Orderのインポートは忘れずに

@shared_task
def send_order_confirmation_email_task(order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.user.refresh_from_db()

        # --- 手動で接続を確立して送信 ---
        # settings.pyから接続設定を取得
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            
            # ユーザー向けメール
            user_subject = "【テスト】ユーザー向けメール"
            user_body = "これはユーザー向けのテストです。"
            user_email = EmailMessage(
                user_subject,
                user_body,
                settings.DEFAULT_FROM_EMAIL,
                [order.user.email],
                connection=connection # この接続を使う
            )
            user_email.send()
            print("ユーザー向けメールを送信しようとしました。")
            
            # 管理者向けメール
            admin_subject = "【テスト】管理者向けメール"
            admin_body = "これは管理者向けのテストです。"
            # mail_adminsの代わりに、ADMINSに直接送信
            admin_recipients = [admin[1] for admin in settings.ADMINS]
            if admin_recipients:
                admin_email = EmailMessage(
                    admin_subject,
                    admin_body,
                    settings.DEFAULT_FROM_EMAIL,
                    admin_recipients,
                    connection=connection # この接続を使う
                )
                admin_email.send()
                print("管理者向けメールを送信しようとしました。")

        return f"Manually sent emails for order {order_id}"

    except Exception as e:
        print(f"タスク内でエラー発生: {e}")
        raise e