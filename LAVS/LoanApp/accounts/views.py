#important notes
#--------------------make an entire "class based view" for the admin interface--------------------
#--------------------make an entire "class based view" for the applicants interface--------------------
from django.shortcuts import render, redirect
from .models import *
from .forms import PolicyForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username Or Password is incorrect')
                return render(request, 'accounts/login.html', )
        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    applicants = Applicant.objects.all()
    policies   = Policy.objects.all()
    context = {
        'work' : 'Home Page',
        'applicants': applicants,
        'policies': policies,
    }    
    return render(request, 'accounts/home.html', context)


def products(request):
	products = Policy.objects.all()

	return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
def admin_page(request):
    applicants = Applicant.objects.all().order_by('id') 
    policies = Policy.objects.all().order_by('id')
    context = {
        'work': 'ADMIN',
        'applicants': applicants,
        'policies': policies,
    }
    return render(request, 'accounts/policy_admin_pages/adminpage.html', context)


@login_required(login_url='login')
def applicant_policy(request, pk_test): #profile page of the applicant
    customer = Applicant.objects.get(id=pk_test)
    orders = customer.policy_set.all()
    order_count = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'accounts/Applicant_page/applicantpage.html', context)

#The amount of payments and applicants page related stuff is here below
@login_required(login_url='login')
def applying_for_policy(request, pk): #Change this name to loan Calc
    customer = Policy.objects.get(id=pk)
    customer_income = customer.applicant.income
    customer_CIBIL_score = customer.applicant.CIBIL_score
    customer_loan_amount = customer.loan_amount
    #-+-+-+-+-+-+-The code for loan begins here-+-+-+-+-+-+-
    principal =  customer.loan_amount   
    interest_rate =  5#This is byDefault   
    duration = customer.Tenure  
    customer_process_fee = customer.Processing_Fees

    # ---function for monthly loan amount calculation---
    def monthly_loan(principal, interest_rate, duration):
        n = duration*12  # total number of months
        r = interest_rate/(100*12)  # interest per month
        # formula for compound interest applied on mothly payments.
        monthly_payment = principal*((r*((r+1)**n))/(((r+1)**n)-1))
        return monthly_payment

    # ---funtion for remaining loan balance calculation---
    def remaining_bal(principal, annual_interest_rate, duration, payments):
        r = annual_interest_rate/1200  # monthly interest rate
        m = r + 1
        n = duration*12  # duration in months
        # remaining balance using compound interest formula
        remaining = principal*(((m**n)-(m**payments))/((m**n)-1))
        return remaining


    monthly = monthly_loan(principal, interest_rate, duration)

    print("Loan amount: ", principal, " Interest rate: ", interest_rate)

    print("Duration (Years): ", duration, " Monthly payment: ", int(monthly))
    
    years_List = []
    Balance_remaining_List = []
    Total_payments_List = []
    for x in range(1, duration+1):
        mon = x*12
        rem = remaining_bal(principal, interest_rate, duration, mon)
        years_List.append(x)
        Balance_remaining_List.append(int(rem))
        Total_payments_List.append(int(monthly*mon))
        print("Year: ", x, " Balance remaining: ", int(rem), " Total payments: ", int(monthly*mon))

    x = zip(years_List, Balance_remaining_List, Total_payments_List)

    context = {
        'x':x,
        'Loan_amount': customer_loan_amount,
        'interest_rate': interest_rate,
        'duration': duration,
        'monthly_payment': monthly,
        'proceesing_Fees': customer_process_fee,
    }
    return render(request, 'accounts/Applicant_page/payments.html', context)
        


@login_required(login_url='login') #Change this name to loan Calc
def createPolicy(request):
    form = PolicyForm()
    if request.method == "POST":
        print('Printing POST:', request.POST)
        form = PolicyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {
        'form':form,
    }
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
def updatePolicy(request, pk):
    order = Policy.objects.get(id=pk)
    form = PolicyForm(instance=order)
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = PolicyForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


