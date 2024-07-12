# Accounting_button/views.py

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as AuthLoginView


class LoginView(AuthLoginView):
    template_name = 'Accounting_button/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard_redirect')



@method_decorator(login_required, name='dispatch')
class DashboardRedirectView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == 'owner':
            return redirect('owner_dashboard')
        elif user.user_type == 'organizer':
            return redirect('organizer_dashboard')
        elif user.user_type == 'executor':
            return redirect('executor_dashboard')
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class OwnerDashboardView(TemplateView):
    template_name = 'Accounting_button/owner_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'owner':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class OrganizerDashboardView(TemplateView):
    template_name = 'Accounting_button/organizer_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'organizer':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ExecutorDashboardView(TemplateView):
    template_name = 'Accounting_button/executor_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'executor':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from .models import PositionDirectory, TariffDirectory, StaffSchedule



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

# Список всех должностей
@method_decorator(owner_or_organizer_required, name='dispatch')
class PositionDirectoryListView(ListView):
    model = PositionDirectory
    template_name = 'Accounting_button/positions_list.html'

# Детали конкретной должности
@method_decorator(owner_or_organizer_required, name='dispatch')
class PositionDirectoryDetailView(DetailView):
    model = PositionDirectory
    template_name = 'Accounting_button/position_detail.html'

# Создание новой должности (только для собственников)
@method_decorator(owner_required, name='dispatch')
class PositionDirectoryCreateView(CreateView):
    model = PositionDirectory
    template_name = 'Accounting_button/position_form.html'
    fields = ['position', 'comments']
    success_url = reverse_lazy('positions_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = self
        context['title'] = 'Create Position'
        return context

# Редактирование существующей должности (только для собственников)
@method_decorator(owner_required, name='dispatch')
class PositionDirectoryUpdateView(UpdateView):
    model = PositionDirectory
    template_name = 'Accounting_button/position_form.html'
    fields = ['position', 'comments']
    success_url = reverse_lazy('positions_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = self
        context['title'] = 'Edit Position'
        return context

# Удаление существующей должности (только для собственников)
@method_decorator(owner_required, name='dispatch')
class PositionDirectoryDeleteView(DeleteView):
    model = PositionDirectory
    template_name = 'Accounting_button/position_confirm_delete.html'
    success_url = reverse_lazy('positions_list')


# Список всех тарифов
@method_decorator(owner_or_organizer_required, name='dispatch')
class TariffDirectoryListView(ListView):
    model = TariffDirectory
    template_name = 'Accounting_button/tariffs_list.html'  # Исправлено

# Детали конкретного тарифа
@method_decorator(owner_or_organizer_required, name='dispatch')
class TariffDirectoryDetailView(DetailView):
    model = TariffDirectory
    template_name = 'Accounting_button/tariff_detail.html'  # Исправлено

# Создание нового тарифа (только для собственников)
@method_decorator(owner_required, name='dispatch')
class TariffDirectoryCreateView(CreateView):
    model = TariffDirectory
    template_name = 'Accounting_button/tariff_form.html'  # Исправлено
    fields = ['tariff_name', 'cost_per_minute', 'comments']
    success_url = reverse_lazy('tariffs_list')

# Редактирование существующего тарифа (только для собственников)
@method_decorator(owner_required, name='dispatch')
class TariffDirectoryUpdateView(UpdateView):
    model = TariffDirectory
    template_name = 'Accounting_button/tariff_form.html'  # Исправлено
    fields = ['tariff_name', 'cost_per_minute', 'comments']
    success_url = reverse_lazy('tariffs_list')

# Удаление существующего тарифа (только для собственников)
@method_decorator(owner_required, name='dispatch')
class TariffDirectoryDeleteView(DeleteView):
    model = TariffDirectory
    template_name = 'Accounting_button/tariff_confirm_delete.html'  # Исправлено
    success_url = reverse_lazy('tariffs_list')




# Список всего штатного расписания
from django.shortcuts import render
from django.views.generic import ListView
from .models import StaffSchedule

@method_decorator(owner_or_organizer_required, name='dispatch')
class StaffScheduleListView(ListView):
    model = StaffSchedule
    template_name = 'Accounting_button/staff_schedule_list.html'  # Исправлено

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_quantity = sum(schedule.quantity for schedule in self.object_list)
        total_working_time_minutes = sum(schedule.total_working_time for schedule in self.object_list)
        total_salary_fund = sum(schedule.total_salary_fund for schedule in self.object_list)
        total_working_time_hours = total_working_time_minutes // 60
        context['total_quantity'] = total_quantity
        context['total_working_time_minutes'] = total_working_time_minutes
        context['total_working_time_hours'] = total_working_time_hours
        context['total_salary_fund'] = total_salary_fund
        return context


# Детали конкретного штатного расписания
@method_decorator(owner_or_organizer_required, name='dispatch')
class StaffScheduleDetailView(DetailView):
    model = StaffSchedule
    template_name = 'Accounting_button/staff_schedule_detail.html'  # Исправлено

# Создание нового штатного расписания (только для собственников)
@method_decorator(owner_required, name='dispatch')
class StaffScheduleCreateView(CreateView):
    model = StaffSchedule
    template_name = 'Accounting_button/staff_schedule_form.html'  # Исправлено
    fields = ['position', 'tariff', 'quantity', 'norm_time_per_month']
    success_url = reverse_lazy('staff_schedule_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.total_working_time = obj.quantity * obj.norm_time_per_month
        obj.total_salary_fund = obj.total_working_time * obj.tariff.cost_per_minute
        obj.save()
        return super().form_valid(form)

# Редактирование существующего штатного расписания (только для собственников)
@method_decorator(owner_required, name='dispatch')
class StaffScheduleUpdateView(UpdateView):
    model = StaffSchedule
    template_name = 'Accounting_button/staff_schedule_form.html'  # Исправлено
    fields = ['position', 'tariff', 'quantity', 'norm_time_per_month']
    success_url = reverse_lazy('staff_schedule_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.total_working_time = obj.quantity * obj.norm_time_per_month
        obj.total_salary_fund = obj.total_working_time * obj.tariff.cost_per_minute
        obj.save()
        return super().form_valid(form)

# Удаление существующего штатного расписания (только для собственников)
@method_decorator(owner_required, name='dispatch')
class StaffScheduleDeleteView(DeleteView):
    model = StaffSchedule
    template_name = 'Accounting_button/staff_schedule_confirm_delete.html'  # Исправлено
    success_url = reverse_lazy('staff_schedule_list')
