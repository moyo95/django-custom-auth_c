from django.contrib import admin
from .models import Item, OrderItem, Order, Payment

# ItemAdminは現状のままでも良いですが、検索やフィルタを追加すると便利です
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'item_number') # 表示するフィールド
    search_fields = ('title', 'item_number') # タイトルと商品番号で検索できるようにする
    list_filter = ('category',) # カテゴリで絞り込めるようにする
    readonly_fields = ('item_number',)


# OrderItemをOrderの詳細画面内で表示するための設定
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # インラインでは、詳細な情報を読み取り専用で表示するのが一般的
    readonly_fields = ('item', 'quantity', 'display_total_price') 
    # 新しいOrderItemをこの画面から追加できないようにする
    can_delete = False 
    max_num = 0 # 追加フォームを非表示にする

    # モデルにない情報を表示するためのカスタムメソッド
    def display_total_price(self, obj):
        # モデルに定義されている get_total_item_price() を呼び出す
        return f"¥{obj.get_total_item_price()}"
    display_total_price.short_description = '小計'


# Orderモデルの管理画面をカスタマイズする設定
class OrderAdmin(admin.ModelAdmin):
    # 注文一覧画面に表示するフィールド
    list_display = (
        'id', 
        'user_info', # ユーザー情報を分かりやすく表示するカスタムメソッド
        'ordered_date', 
        'display_total_order_price',
        'ordered', # 支払い済みかどうか
    )
    # 支払い状況と注文日で絞り込みできるようにする
    list_filter = ('ordered', 'ordered_date')
    # ユーザーのメールアドレスや注文IDで検索できるようにする
    search_fields = ('user__email', 'id')
    # 注文詳細画面に、関連するOrderItemの一覧を表示する
    inlines = [OrderItemInline]
    # 注文詳細画面で読み取り専用にするフィールド
    readonly_fields = ('user', 'ordered_date', 'payment')

    # カスタムメソッドの定義
    def user_info(self, obj):
        return obj.user.email if obj.user else 'N/A'
    user_info.short_description = '顧客メールアドレス' # 一覧の列名

    def display_total_order_price(self, obj):
        return f"¥{obj.get_total()}"
    get_total.short_description = '合計金額' # 一覧の列名


# Paymentモデルも少し見やすく
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')
    readonly_fields = ('user', 'amount', 'timestamp', 'stripe_charge_id')


# --- モデルと設定クラスを登録 ---

# 元の登録はいったん削除し、新しい設定クラスで登録し直す
# admin.site.register(Item)
# admin.site.register(OrderItem)
# admin.site.register(Order)
# admin.site.register(Payment)

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)

# OrderItemはOrderAdminのinlinesで使っているので、単独で登録する必要はありません。
# もし単独でも見たい場合は、コメントを外してください。
# admin.site.register(OrderItem)