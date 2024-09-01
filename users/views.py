import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserResetPassword(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'users/generate.html'
    success_url = 'users:login'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        if user:
            password = User.objects.make_random_password(length=10)
            user.set_password(password)
            user.save()
            send_mail(
                subject='Смена пароля',
                message=f'Привет, новый пароль - {user.password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        return redirect(reverse('users:login'))


class UserListView(ListView, LoginRequiredMixin):
    model = User


class UserDetailView(DetailView, LoginRequiredMixin):
    model = User


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@permission_required('users.deactivate_user')
def toggle_activity(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:users_list'))
