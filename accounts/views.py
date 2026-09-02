
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.db.models import Q

from admissions.models import *


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    next_page = reverse_lazy("dashboard")
    
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_applications"] = 0
        context["pending_applications"] = 0
        context["approved_applications"] = 0
        context["applications_today"] = 0

        return context
    
    
class ApplicationsView(LoginRequiredMixin, TemplateView):
    template_name = "applications/applications.html"
    
    
class StudentListView(ListView):
    model = Application
    template_name = "students/students.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Application.objects
            .prefetch_related("documents")
            .select_related("education__highest_qualification")
            .order_by("-created_at")
        )

        search = self.request.GET.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(application_number__icontains=search)
                | Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(mobile__icontains=search)
                | Q(father_name__icontains=search)
                | Q(father_mobile__icontains=search)
                | Q(mother_name__icontains=search)
                | Q(mother_mobile__icontains=search)
            )

        return queryset


class DocumentsView(LoginRequiredMixin, TemplateView):
    template_name = "documents/documents.html"


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = "users/users.html"


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings/settings.html"