from django.contrib import admin
from .models import Item, OrderItem, Order, Payment

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'item_number')
    search_fields = ('title', 'item_number')
    list_filter = ('category',)
    readonly_fields = ('item_number',)

# OrderAdminを修正
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user_info',
        'ordered_date', 
        'display_total_order_price', # カスタムメソッド名
        'ordered',
    )
    list_filter = ('ordered', 'ordered_date')
    search_fields = ('user__email', 'id')

    # ManyToManyFieldはインライン表示が複雑なので、
    # readonly_fieldsで表示する方がシンプルで確実
    readonly_fields = ('user', 'ordered_date', 'payment', 'display_ordered_items')

    # 表示用のフィールドセットを定義
    fieldsets = (
        ('注文情報', {
            'fields': ('id', 'user', 'ordered', 'ordered_date', 'payment')
        }),
        ('注文商品', {
            'fields': ('display_ordered_items',),
        }),
    )

    # 読み取り専用のIDも表示する
    readonly_fields = ('id',) + readonly_fields

    # --- カスタムメソッドの定義 ---

    def user_info(self, obj):
        return obj.user.email if obj.user else 'N/A'
    user_info.short_description = '顧客'

    # 合計金額を表示するメソッド
    def display_total_order_price(self, obj):
        return f"¥{obj.get_total()}"
    display_total_order_price.short_description = '合計金額'

    # 注文商品リストをHTMLで整形して表示するメソッド
    def display_ordered_items(self, obj):
        from django.utils.html import format_html
        
        # 注文された商品を取得
        items = obj.items.all()
        if not items:
            return "（商品なし）"

        # HTMLの箇条書きリストを作成
        html = "<ul>"
        for order_item in items:
            html += f"<li>{order_item.item.title} x {order_item.quantity}  (小計: ¥{order_item.get_total_item_price()})</li>"
        html += "</ul>"
        return format_html(html)
    display_ordered_items.short_description = '商品リスト'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')
    readonly_fields = ('user', 'amount', 'timestamp', 'stripe_charge_id')


# --- モデルの登録 ---
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
# OrderItemはOrder詳細画面で見るので、単独登録は不要なことが多い
# admin.site.register(OrderItem)