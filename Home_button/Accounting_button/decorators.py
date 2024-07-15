from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Декоратор для проверки, что пользователь не является исполнителем
def executor_forbidden(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 'executor':
            return redirect('forbidden')  # Перенаправление на страницу с сообщением о недостаточности прав
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Декоратор для проверки, что пользователь является собственником
def owner_required(view_func):
    @login_required
    @executor_forbidden
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type != 'owner':
            return redirect('forbidden')  # Перенаправление на страницу с сообщением о недостаточности прав
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Декоратор для проверки, что пользователь является собственником или организатором
def owner_or_organizer_required(view_func):
    @login_required
    @executor_forbidden
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type not in ['owner', 'organizer']:
            return redirect('forbidden')  # Перенаправление на страницу с сообщением о недостаточности прав
        return view_func(request, *args, **kwargs)
    return _wrapped_view
