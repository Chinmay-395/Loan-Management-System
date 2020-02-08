from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('adminpage/',views.admin_page, name='adminpage'),
    path('applicant_policy/<str:pk_test>/', views.applicant_policy, name="applicant_policy"),
    #The following path is for calculating the loan needed to be paid for that policy
    path('applying_for_policy/<str:pk>/',views.applying_for_policy, name="applying_for_policy"),
    #practice URL
    #path('')
    #This shows a table for all the policies
    path('products/', views.products, name='products'),
    #path('customers/', views.customers, ),
    path('createPolicy/', views.createPolicy, name="createPolicy"),
    path('updatePolicy/<str:pk>/', views.updatePolicy, name="updatePolicy"),
    
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    
]
