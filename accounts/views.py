import stripe
from django.conf import settings
from django.views import View
from django.http import JsonResponse

from django.shortcuts import render, redirect
# from django.views import View
from accounts.models import CustomUser
from accounts.forms import ProfileForm
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin


# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordContextMixin


from django.contrib.auth.forms import PasswordResetForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.base import TemplateView,RedirectView
from django.contrib.auth.forms import SetPasswordForm
import django.contrib.auth.mixins  # この行を追加
# views.py でのインポート文を以下のように修正
# from django.views.generic import TemplateView

from django.shortcuts import render
from django.views.generic import TemplateView
from allauth.account import views 
# from .forms import CustomSignupForm
from django.contrib.auth import login
from django.http import HttpResponse # このimportが必要な場合は追加してください

def signup_view(request):
    return HttpResponse("サインアップページのテスト表示")

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        
        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })

# class ProfileEditView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         user_data = CustomUser.objects.get(id=request.user.id)
#         form = ProfileForm(
#             request.POST or None,
#             initial = {
#                 'first_name': user_data.first_name,
#                 'last_name': user_data.last_name,
#                 user.first_name_kana = form.cleaned_data.get('first_name_kana')
#                 user.last_name_kana = form.cleaned_data.get('last_name_kana')
#                 user.postal_code = form.cleaned_data.get('postal_code')
#                 user.address1 = form.cleaned_data.get('address1')
#                 user.address2 = form.cleaned_data.get('address2')
#                 'tel': user_data.tel,
#             }
#         )

#         return render(request, 'accounts/profile_edit.html', {
#             'form':form
#         })
    
#     def post(self, request, *args, **kwargs):
#         form = ProfileForm(request.POST or None)
#         if form.is_valid():
#             user_data = CustomUser.objects.get(id=request.user.id)
#             user_data.first_name = form.cleaned_data['first_name']
#             user_data.last_name = form.cleaned_data['last_name']
#             user_data.address = form.cleaned_data['address']
#             user_data.tel = form.cleaned_data['tel']
#             user_data.save()
#             return redirect('profile')
        
#         return render(request, 'accounts/profile.html',{
#             'form': form,
#             'user_data': user_data,
#         })

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(initial={
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'first_name_kana': user_data.first_name_kana,
            'last_name_kana': user_data.last_name_kana,
            'postal_code': user_data.postal_code,
            'address1': user_data.address1,
            'address2': user_data.address2,
            'tel': user_data.tel,
        })
        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.first_name_kana = form.cleaned_data['first_name_kana']
            user_data.last_name_kana = form.cleaned_data['last_name_kana']
            user_data.postal_code = form.cleaned_data['postal_code']
            user_data.address1 = form.cleaned_data['address1']
            user_data.address2 = form.cleaned_data['address2']
            user_data.tel = form.cleaned_data['tel']
            user_data.save()
            
            # 【修正点1】リダイレクト先には名前空間 'accounts:' を付ける
            return redirect('accounts:profile')

        # 【修正点2】フォームが無効だった場合は、エラー情報を持ったフォームを
        #            「編集ページ」のテンプレートで再表示する
        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })
    
# class LoginView(views.LoginView):
#         template_name = 'accounts/login.html'


# class LogoutView(views.LogoutView):
#      template_name = 'accounts/logout.html'

#      def post(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#                self.logout()
#         return redirect('/')
     
# class SignupView(views.SignupView):
#      template_name = 'accounts/signup.html'
#      form_class = SignupUserForm


# class PasswordResetView(PasswordContextMixin, FormView):
#     email_template_name = 'registration/password_reset_email.html'
#     extra_email_context = None
#     form_class = PasswordResetForm
#     from_email = None
#     html_email_template_name = None
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'registration/password_reset_form.html'
#     title = ('Password reset')
#     token_generator = default_token_generator


# class PasswordResetDoneView(PasswordContextMixin, TemplateView):
#     template_name = 'registration/password_reset_done.html'
#     title = ('Password reset sent')

# class PasswordResetConfirmView(PasswordContextMixin, FormView):
#     form_class = SetPasswordForm
#     post_reset_login = False
#     post_reset_login_backend = None
#     reset_url_token = 'set-password'
#     success_url = reverse_lazy('password_reset_complete')
#     template_name = 'registration/password_reset_confirm.html'
#     title = ('Enter new password')
#     token_generator = default_token_generator

# class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
#     template_name = 'registration/password_reset_complete.html'
#     title = ('Password reset complete')


# class EmailVerificationSentView(views.EmailVerificationSentView):
#     template_name = 'accounts/confirm-email.html'

# class AccountConfirmEmailView(RedirectView):
#     url = 'confirm-email/'  # リダイレクト先のURL

# stripe.api_key = settings.STRIPE_SECRET_KEY

# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': 'jpy',
#                     'product_data': {
#                         'name': '商品名',
#                     },
#                     'unit_amount': 2000,  # 金額（円 x 100）
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url='http://localhost:8000/success/',
#             cancel_url='http://localhost:8000/cancel/',
#         )
#         return JsonResponse({'id': session.id})
# class EmailVerificationSentView(views.EmailVerificationSentView):
#     template_name = 'accounts/confirm-email.html'

# def signup_view(request):
#     if request.method == 'POST':
#         form = CustomSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('app:item_list') # 登録後のリダイレクト先
#     else:
#         form = CustomSignupForm()
        
#     return render(request, 'account/signup.html', {'form': form})