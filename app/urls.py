# app/urls.py

from django.urls import path
from . import views
# from django.views.generic import TemplateView

app_name = 'app'

urlpatterns = [
    # 商品一覧ページ
    path('', views.ItemListView.as_view(), name='item_list'), 
    
    # 商品詳細ページ
    path('product/<slug:slug>/', views.ItemDetailView.as_view(), name='product'),
    
    # カート追加機能
    path('add-item/<slug:slug>/', views.addItem, name='additem'),
    
    # 注文概要ページ
    path('order/', views.OrderView.as_view(), name='order'),
    
    # カートからアイテムを削除
    path('remove-item/<slug:slug>/', views.removeItem, name='removeitem'),
    
    # カートのアイテムを1つ減らす
    path('remove-single-item/<slug:slug>/', views.removeSingleItem, name='removesingleitem'),
    
    # 決済ページ
    path('payment/', views.PaymentView.as_view(), name='payment'),
    
    # 決済完了ページ
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    
    # Stripe Checkout Session作成のエンドポイント
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),

    # path('cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
    # path('cancel/', TemplateView.as_view(template_name="app/cancel.html"), name="payment_cancel"),
]