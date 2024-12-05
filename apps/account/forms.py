import re 
from django import forms
from django.contrib.auth import get_user_model
from apps.main.models import Contact



User = get_user_model()



class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    


    class Meta:
        model = User
        fields = ["email", "first_name", "middle_name", "last_name", "password", "confirm_password"]
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class" : "form-control"})

        
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data["password"] != cleaned_data["confirm_password"]:
            raise forms.ValidationError("Passwords didn't match")
        return super().clean()

        # def clean_password1(self):
        #     password1 = self.cleaned_data.get("password1")
        #     print(password1)
        #     if len(password1) < 8:
        #         print("length validation")
        #         raise forms.ValidationError("Password must be 8 characters long!")
        #     if not re.search(r'\d', password1) or not re.search(r'[A-Za-z]', password1):
        #         print("numbers and chars")
        #         raise forms.ValidationError("Password must contain both numbers and characters.")
        #     return password1


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget = forms.PasswordInput() )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class" : "form-control"})




class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=14)
    profile_picture = forms.FileField(required=False)
    address = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea())
    resume = forms.FileField(required=False)

    def validate(self):
        print("In resume")
        cleaned_data = self.cleaned_data
        resume = self.cleaned_data.get("resume")
        if resume:
            extension = resume.name.split(".")[-1]  # resume.pdf  ["resume", "pdf"]
            if extension not in ["pdf", "PDF"]:
                raise forms.ValidationError("Please upload resume in pdf !")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            try:
                profile = user.userprofile
            except:
                pass
            else:
                self.fields["phone_number"].initial = profile.phone_number
                self.fields["profile_picture"].initial = profile.profile_picture
                self.fields["address"].initial = profile.address
                self.fields["bio"].initial = profile.bio
                self.fields["resume"].initial = profile.resume
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "company_name", "email", "phone_number", "message"]
                
