"""
URL configuration for Stock_Market_Analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include

#For LoginPage
from LoginPage.views import signup, login, homepage, transaction, stock, account, test

#For HomePage
# from HomePage.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    #For HomePage
    # path('homepage/', HomeView, name='homepage'),

    #For signup
    path('signup/', signup, name='signup'),  
    #For login
    path('', login, name='login'),  

    path('homepage/', homepage, name='homepage'),  

    path('homepage/transaction/', transaction, name='transaction'), 
    path('homepage/stock/', stock, name='stock'),  
    path('homepage/account/', account, name='account'), 
    path('test/', test, name='test'),

]
