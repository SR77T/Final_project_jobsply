from django.urls import path
from . import views

urlpatterns = [
    path("job/detail/<int:pk>/", views.JobDetailView.as_view(), name = "job_detail"),
    path("apply-job/<int:job_id>/", views.ApplyJobView.as_view(), name = "apply_job"),
    path("my-jobs/", views.MyJobs.as_view(), name = "my_jobs"),
    path("about-us/", views.AboutUs.as_view(), name = "about_us"),
    

    path("contact-us/", views.ContactView.as_view(), name="contact_us"),




    path("", views.HomePageView.as_view(), name = "home_page"),

]