from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('adminpage/',views.admin_page, name='adminpage'),
    path('updateApplicant/<str:pk>/',views.updateCustomer, name='updateApplicant'),
    # '''
    # applicant_policy --> The below path needs to send the "applicant number"
    # applying_for_policy --> The below path needs to send the "policy number"
    # '''
    path('applicant_policy/<str:pk_of_applicant>/',
         views.applicant_policy, name="applicant_policy"),
    #The following path is for calculating the loan needed to be paid for that policy
    path('applying_for_policy/<str:pk>/',views.applying_for_policy, name="applying_for_policy"),
    #practice URL
    path('user/', views.userPage, name='user-page'),
    #This shows a table for all the policies
    path('products/', views.products, name='products'),
    #path('customers/', views.customers, ),
    path('createPolicy/', views.createPolicy, name="createPolicy"),
    path('updatePolicy/<str:pk>/', views.updatePolicy, name="updatePolicy"),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

     # path('applying_for_policy_Evaluator/<str:pk>/',views.applying_for_policy_Evaluator, name='applying_for_policy_Evaluator'),
     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
     path('addPolicy/<str:pk>/',views.addPolicy, name='addPolicy'),
     #!!!!!!!!!!!!!!!!!
     path('CheckingOnApplicant/<str:pk>/', views.CheckingOnApplicant,
         name="CheckingOnApplicant"),
     #######Authentication password reset     
     path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

     path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
     name="password_reset_done"),

     path('reset/<uidb64>/<token>',
     auth_views.PasswordResetConfirmView.as_view( template_name="accounts/password_reset_form.html"),
     name="password_reset_confirm"),

     path('reset_password_complete/', 
     auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
     name="password_reset_complete"),
]
#######Authentication password reset steps
'''
     1 - Submit email form                        //PasswordResetView.as_view()
     2 - Email sent success message               //PasswordResetDoneView.as_view()
     3 - Link to Password reset form in email     //PasswordResetConfirmView.as_view()
     4 - Password successfully changed message    //PasswordResetCompleteView.as_view()
     '''
