# app/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email_task(order_id):
    """注文完了メールを非同期で送信するタスク"""
    try:
        order = Order.objects.get(id=order_id)
        subject = render_to_string('app/email/order_confirmation_subject.txt', {'order': order}).strip()
        body = render_to_string('app/email/order_confirmation_body.txt', {'order': order, 'user': order.user})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=False,
        )
        return f"Successfully sent email for order {order_id}"
    except Order.DoesNotExist:
        return f"Error: Order with id={order_id} not found."
    except Exception as e:
        # Celeryのリトライ機能に任せるため、例外を再発生させる
        raise e