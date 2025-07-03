from django.db import models
from django.conf import settings
from django.utils import timezone

class Item(models.Model):
    title = models.CharField(max_length=100)
    item_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    def save(self, *args, **kwargs):
        if not self.item_number:
            # 連番取得
            last_item = Item.objects.order_by('-id').first()
            next_number = 1
            if last_item and last_item.item_number:
                try:
                    # フォーマット A-0001-001 → 末尾の数値部分を抽出して +1
                    last_serial = int(last_item.item_number.split('-')[-1])
                    next_number = last_serial + 1
                except (IndexError, ValueError):
                    next_number = 1

            # ここで商品IDを構築（例: A-0001-001）
            group_code = "0001"  # 固定コード or カテゴリーなどから動的生成可
            prefix = "A"
            serial_code = str(next_number).zfill(3)
            self.item_number = f"{prefix}-{group_code}-{serial_code}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def __str__(self):
        return f'{self.item.title}:{self.quantity}'
    
    def get_subtotal(self):
        return self.item.price * self.quantity
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField(null=True, blank=True)

    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
    
    def __str__(self):
        return self.user.email


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_change_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    

