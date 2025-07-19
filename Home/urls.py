from django.urls import path 
from .import views  

from django.contrib.auth.views import LogoutView

urlpatterns = [

    path("Index",views.Index,name="Index"),
    path('',views.SignIn,name="SignIn"),
    path('SignOut', views.SignOut, name='SignOut'),
    path('profile', views.profile, name='profile'),
    path("get_monthly_data/",views.get_monthly_data,name="get_monthly_data"),
    path("get_monthly_revenue_expense/",views.get_monthly_revenue_expense,name="get_monthly_revenue_expense"),
    path("add-staff/",views.add_staff,name="add_staff"),
    path("list_staff/",views.list_staff,name="list_staff"),
    path("add_customers/",views.add_customers,name="add_customers"),
    path("delete_staff/<int:pk>/",views.delete_staff,name="delete_staff"),
    path("update_staff/<int:pk>/",views.update_staff,name="update_staff"),
    path("list_salary",views.list_salary,name="list_salary"),
    path("add_salary",views.add_salary,name="add_salary"),
    path("delete_staff_salary/<int:pk>",views.delete_staff_salary,name="delete_staff_salary"),

    path("notification_read/<int:pk>",views.notification_read,name="notification_read"),
    path("clear_notification",views.clear_notification,name="clear_notification")

    
]