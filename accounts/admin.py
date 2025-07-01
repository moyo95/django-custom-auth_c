# from django.contrib import admin
# from .models import CustomUser



# admin.site.register(CustomUser)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser

#     # ordering と list_display を修正（username を使わない）
#     ordering = ['email']  # 例：メールアドレスでソート
#     list_display = ['email', 'first_name', 'last_name']  # 表示したいフィールドを記述

#     fieldsets = UserAdmin.fieldsets + (
#         ('追加情報', {
#             'fields': (
#                 'first_name_kana',
#                 'last_name_kana',
#                 'postal_code',
#                 'address1',
#                 'address2',
#                 'tel',
#             ),
#         }),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)

# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # 【1. ユーザー編集画面のカスタマイズ】
    # ここがエラーの直接の原因。username と date_joined を使わないように再定義する。
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": (
            "first_name", 
            "last_name", 
            "first_name_kana", 
            "last_name_kana",
            "postal_code",
            "address1",
            "address2",
            "tel",
        )}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}), # date_joined は削除
    )

    # 【2. ユーザー追加画面のカスタマイズ】
    # これも username を使わないようにする。
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password2"), # 新規作成時の入力項目
            },
        ),
    )

    # 【3. 一覧画面のカスタマイズ】
    # これで「メールアドレスしか見えない」問題が解決する。
    list_display = ("email", "first_name", "last_name", "is_staff")
    
    # 【4. 検索ボックスの対象フィールド】
    search_fields = ("email", "first_name", "last_name")

    # 【5. 並び順】
    ordering = ("email",)

    # 【6. その他】
    # UserAdminがデフォルトで持っているusername関連の機能を無効化
    filter_horizontal = ()
    list_filter = ()


admin.site.register(CustomUser, CustomUserAdmin)