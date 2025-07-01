# accounts/adapter.py

from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        allauthのデフォルトの save_user をオーバーライドして、
        emailが確実にセットされるように保証する。
        """
        # まず、親クラスの save_user を呼び出す。
        # これにより、パスワードなどの基本的な設定が行われる。
        user = super().save_user(request, user, form, commit=False)
        
        # email がセットされていない場合に備え、フォームから明示的に取得してセットする。
        user.email = form.cleaned_data.get('email')
        
        # データベースに保存する
        if commit:
            user.save()
            
        return user


    def populate_username(self, request, user):
        """
        usernameを生成しようとする処理は、引き続き無効化する。
        """
        pass