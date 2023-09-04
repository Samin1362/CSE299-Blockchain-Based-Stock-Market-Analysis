from django.shortcuts import render, redirect
from django.views import View
from .models import LoginPage

# Create your views here.
class LoginPageDetailView(View):
    template_name = 'Login_Page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request, *args, **kwargs):
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')

        try:
            user = LoginPage.objects.get(username=username_, password=password_)
        except LoginPage.DoesNotExist:
            return render(request, self.template_name, {'error_message':'Invalid username or Password'})
        
        return redirect('homepage')