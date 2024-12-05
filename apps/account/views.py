from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, View, DetailView, UpdateView
from .forms import UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import send_email_activation
from django.contrib.auth import get_user_model
from .models import UserAccountActivation, UserProfile
from .forms import UserProfileForm


User = get_user_model()





# Create your views here.
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "account/user_register.html"
    # success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        password = form.cleaned_data.pop("password")
        confirm_password = form.cleaned_data.pop("confirm_password")
        user = form.save()
        user.set_password(password)
        user.save()
        send_email_activation(user, self.request)
        messages.success(self.request, "User created successfully!")
        return redirect("home_page")

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't add user!")
        return super().form_invalid(form)


class UserLoginView(FormView):
    form_class =  UserLoginForm
    template_name = "account/user_login.html"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, email = email, password = password)
        if user:
            login(self.request, user)
            messages.success(self.request, "User logged in!")
            return redirect("home_page")
        messages.error(self.request, "Invalid credentials!")
        return redirect("user_login")


def user_Logout(request):
    logout(request)
    messages.success(request, "User logged out !")
    return redirect("home_page")

class UserAccountActivationView(View):
    def get(self, *args, **kwargs):
        username = kwargs["username"]
        key = kwargs["key"]
        user = User.objects.filter(username = username)
        if user.exists():
            user = user[0]
            ua = UserAccountActivation.objects.filter(key = key, email = user.email)
            if ua.exists(): 
                user.is_verified = True
                user.save()
                messages.success(self.request, "Account Activated !")
                return redirect("home_page")
        messages.error(self.request, "Invalid activation link !")
        return redirect("user_login")


class ResendEmailActivation(View):
    def get(self, *args, **kwargs):
        send_email_activation(self.request.user, self.request)
        messages.success(self.request, "Activation link resent !")
        return redirect("home_page")


class UserProfileView(DetailView):
    queryset = User.objects.all()
    template_name = "account/user_profile.html"


    # def form_valid(self, form):
    #     # cleaned_data = form.cleaned_data
    #     bio = form.cleaned_data.pop("bio")
    #     phone_number = form.cleaned_data.pop("phone_number")
    #     pp = form.cleaned_data.pop("profile_picture")
    #     student = form.save()
    #     sp, _ = StudentProfile.objects.update_or_create(student = student, defaults = {"bio" : bio, "phone" : phone_number})
    #     if pp:
    #         sp.profile_picture = pp
    #         sp.save()
    #     return redirect("classbased:student_detail", student.id)
    



class UserProfileUpdateView(DetailView, FormView):
    form_class = UserProfileForm
    queryset = User.objects.all()
    template_name = "account/profile_update.html"
    context_object_name = "user"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            user = self.request.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            phone_number = form.cleaned_data.get("phone_number")
            profile_picture = form.cleaned_data.get("profile_picture")
             
            address = form.cleaned_data.get("address")
            bio = form.cleaned_data.get("bio")
            resume = form.cleaned_data.get("resume")

            up, _ = UserProfile.objects.update_or_create(user=user,
                                                         defaults=dict(phone_number=phone_number,
                                                                       address=address,
                                                                       bio=bio))
            up.profile_picture = profile_picture
            up.resume = resume
            up.save()
            messages.success(request, "Profile updated successfully !")
            return redirect("user_profile", request.user.id)
        else:
            messages.error(request, "Couldn't update the user profile !")
            return redirect("update_profile", request.user.id)
    
    
        
        
    
