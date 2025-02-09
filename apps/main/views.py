import requests
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView
from django.contrib import messages
from django.db.models import OuterRef, Exists, Value, Q
from django.urls import reverse_lazy
from .models import Job, JobApplication, APPLIED, Category
from apps.account.forms import ContactForm




class HomePageView(ListView):
    template_name = "main/home.html"
    paginate_by = 6
    context_object_name = 'object_list'

    def get_queryset(self):
        """
        Get all jobs with applied status for authenticated users.
        Exclude recommended jobs from main listing.
        Include search functionality.
        """
        if self.request.user.is_authenticated:
            # Get recommended job IDs to exclude from main listing
            recommended_job_ids = self.get_recommended_job_ids()
            
            applied_jobs = JobApplication.objects.filter(
                user=self.request.user,
                job=OuterRef('pk')
            )
            qs = Job.objects.all().annotate(
                applied=Exists(applied_jobs)
            ).order_by("-created_at")
            
            # Exclude recommended jobs if they exist
            if recommended_job_ids:
                qs = qs.exclude(id__in=recommended_job_ids)
        else:
            qs = Job.objects.all().annotate(
                applied=Value(False)
            ).order_by("-created_at")

        # Handle search functionality
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(location__icontains=search) |
                Q(category__title__icontains=search)
            )

        return qs

    def get_recommended_job_ids(self):
        """
        Helper method to get IDs of recommended jobs.
        """
        if not self.request.user.is_authenticated:
            return None

        applied_categories = JobApplication.objects.filter(
            user=self.request.user
        ).values_list('job__category', flat=True).distinct()

        if not applied_categories:
            return None

        applied_jobs = JobApplication.objects.filter(
            user=self.request.user
        ).values_list('job', flat=True)

        recommended = Job.objects.filter(
            category__in=applied_categories
        ).exclude(
            id__in=applied_jobs
        ).order_by('-created_at')[:3].values_list('id', flat=True)

        return list(recommended)

    def get_recommended_jobs(self):
        """
        Get recommended jobs based on user's applied job categories.
        Returns jobs from similar categories that the user hasn't applied to.
        """
        recommended_job_ids = self.get_recommended_job_ids()
        if not recommended_job_ids:
            return None

        recommended = Job.objects.filter(
            id__in=recommended_job_ids
        ).annotate(
            applied=Value(False)
        ).order_by('-created_at')

        return recommended

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories for filtering
        context["categories"] = Category.objects.all()
        
        # Add recommended jobs if user is authenticated and has applied to jobs
        if self.request.user.is_authenticated:
            has_applied_jobs = JobApplication.objects.filter(
                user=self.request.user
            ).exists()
            context["has_applied_jobs"] = has_applied_jobs
            
            if has_applied_jobs:
                recommended_jobs = self.get_recommended_jobs()
                if recommended_jobs:
                    context["recommended_jobs"] = recommended_jobs

        return context


class JobDetailView(DetailView):
    template_name = "main/job_detail.html"
    queryset = Job.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        if self.request.user.is_authenticated:
            application = JobApplication.objects.filter(user=self.request.user, job=job)
            context["has_applied"] = application.exists()
        return context


class ApplyJobView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_verified:
            messages.error(self.request, "Please verify your email first !")
            return redirect("home_page")
        try:
            if not self.request.user.userprofile.resume:
                messages.error(self.request, "Please upload your resume !")
                return redirect("home_page")
        except:
            messages.error(self.request, "Please complete your profile first !")
            return redirect("home_page")
        job_id = kwargs["job_id"]
        job = Job.objects.get(id=job_id)
        JobApplication.objects.create(job=job, user=self.request.user, status=APPLIED)
        messages.success(self.request, "Successfully applied to the Job !")
        return redirect("home_page")


class MyJobs(ListView):
    template_name = "main/my_jobs.html"

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


class AboutUs(TemplateView):
    template_name = "main/about_us.html"


class ContactView(CreateView):
    form_class = ContactForm
    template_name = "main/contact.html"
    success_url = reverse_lazy("home_page")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "Your response has been recorded. We will get back to you soon !")
            return self.form_valid(form)
        else:
            messages.error(request, "Could not record your response !")
            return self.form_invalid(form)
