from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Регистрация прошла успешно!"))
            return redirect('pages:home')
        else:
            error_message = _("Пожалуйста, исправьте ошибки в форме.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label if field != '__all__' else ''}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form, 'title': _('Регистрация')})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _("Вы успешно вошли в систему."))
                return redirect(request.GET.get('next', 'pages:home'))
            else:
                messages.error(request, _("Неверное имя пользователя или пароль."))
        else:
            messages.error(request, _("Неверное имя пользователя или пароль."))
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'title': _('Вход в систему')})


def logout_view(request):
    logout(request)
    messages.info(request, _("Вы вышли из системы."))
    return redirect('pages:home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Профиль пользователя'),
        })
        return context


class ApplicationsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/applications.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Мои заявки'),
        })
        return context
