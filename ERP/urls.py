"""
URL configuration for ERP project.

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
from ERP.views import LR_VIEW,invoice_view,tax_invoice_form,print_invoice

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',LR_VIEW,name='LR'),
    path('invoice/', invoice_view, name='invoice'),
    path('taxinvoiceform/', tax_invoice_form, name='tax_invoice_form'),
    path('print_invoice/', print_invoice, name='print_invoice')
]
