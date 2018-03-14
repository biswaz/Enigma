from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    college = forms.CharField(help_text='Enter the name of your institution')
    email = forms.EmailField(help_text='Enter you email')
    phone_number = forms.CharField(max_length=10, label='Phone number')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.college = self.cleaned_data['college']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone_number']
        #using phone_number instead of phone might've been a problem
        user.save()
