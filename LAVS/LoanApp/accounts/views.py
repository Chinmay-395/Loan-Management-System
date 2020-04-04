#important notes
#--------------------make an entire "class based view" for the admin interface--------------------
#--------------------make an entire "class based view" for the applicants interface--------------------
from django.shortcuts import render, redirect, get_object_or_404
from .models import Policy, Applicant
from .forms import PolicyForm, CreateUserForm, UpgradeUserForm
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import modelformset_factory, inlineformset_factory 
# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Applicant.objects.create(
                user=user,
                name=user.username,
                email= user.email,
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
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


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])#accessible only to customer[ie who are logged in]
def userPage(request): # this page the for applicants[ie members] 
    customer = request.user.applicant # "request.user.applicant" --> this variable returns name of the applicant who is logged in
    print("Name of the customer using the customer variable, is {}".format(customer))
    #orders = customer.policy_set.all()
    policies_taken_by_applicant = request.user.applicant.policy_set.all()
    print(policies_taken_by_applicant)
    print("The phone no is {}".format(request.user.applicant.phone))

    total_policies = policies_taken_by_applicant.count()
    context = {
        'customer':customer,
        'orders':policies_taken_by_applicant,
        'total_orders': total_policies,
        }
    return render(request, 'accounts/user.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
#@admin_only
def home(request):
    applicants = Applicant.objects.all()
    policies   = Policy.objects.all()
    context = {
        #'work' : 'Home Page',
        'applicants': applicants,
        'policies': policies,
    }
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
	products = Policy.objects.all()

	return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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
def applicant_policy(request, pk_of_applicant): #profile page of the applicant
    #print("The primary key {}".format(gk))
    #customer = get_object_or_404(Applicant,pk=pk_test)
    pk_test = pk_of_applicant
    customer = Applicant.objects.get(id=pk_test)
    orders = customer.policy_set.all()
    order_count = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'accounts/Applicant_page/applicantpage.html', context)


@login_required(login_url='login') #Loan Installments calculator function
def applying_for_policy(request, pk): #calculates the amount that needs to be paid monthly
    customer = Policy.objects.get(id=pk)
    #customer_income = customer.applicant.income
    #customer_CIBIL_score = customer.applicant.CIBIL_score
    customer_loan_amount = customer.loan_amount
    #-+-+-+-+-+-+-The code for loan begins here-+-+-+-+-+-+-
    principal =  customer.loan_amount
    interest_rate =  customer.interest_rate#This is byDefault
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


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])  
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
@allowed_user(allowed_roles=['admin'])
def updatePolicy(request, pk):
    #print(request)
    order = Policy.objects.get(id=pk)
    print(order)
    print(order.id)
    #print(request.user.applicant)
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


def updateCustomer(request, pk):
    applicantToBeUpdated = Applicant.objects.get(id=pk)
    #print(applicantToBeUpdated)
    form = UpgradeUserForm(instance=applicantToBeUpdated)
    if request.method == 'POST':
        form = UpgradeUserForm(request.POST, instance=applicantToBeUpdated)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

#############adding new policy inside the users account#############
def addPolicy(request,pk):#primary key of the 'Policy'
    order = Policy.objects.get(id=pk)
    customer = request.user.applicant
    print(customer)
    print(customer.income)
    try:
        def monthly_loan(principal, interest_rate, duration):
            n = duration*12  # total number of months
            r = interest_rate/(100*12)  # interest per month
            # formula for compound interest applied on mothly payments.
            monthly_payment = principal*((r*((r+1)**n))/(((r+1)**n)-1))
            return monthly_payment
        #based on previous policy monthly payments stuff
        setOfPolicyTakenByMember = customer.policy_set.all()
        sum = 0
        for Every_Policy in setOfPolicyTakenByMember:
            principal = Every_Policy.loan_amount
            interest_rate = 5#add the intrest in the policy; hERE i have given in default
            duration = Every_Policy.Tenure
            #Calculating Monthly payment of using the function define earlier#
            monthly_payment_of_individual_policy = monthly_loan(principal, interest_rate, duration)
            sum = sum + monthly_payment_of_individual_policy
        customer_income_per_month = round(customer.income/12,2)
        if customer_income_per_month > sum: 
        #if the income is more than all the monthly payment of earlier policy then do this
            form = PolicyForm(initial={'applicant': customer,
                                    'policy_name': order.policy_name, 
                                    'bank':order.bank,
                                    'Tenure':order.Tenure,
                                    'Processing_Fees': order.Processing_Fees,
                                    'loan_amount': order.loan_amount})
            if request.method == 'POST':
                print('Printing POST:', request.POST)
                form = PolicyForm(request.POST, instance=order)
                if form.is_valid():
                    form.save()
                    return redirect('/')

            context = {
                'form': form
            }
            print('Successfully applied for the policy if clicked on submit button')
            messages.success(request,"Successfully applied for the policy")
            return render(request, 'accounts/order_form.html', context)
        else:
            print('Insufficient funds')
            messages.info(request,'Insufficient funds')
            return redirect('home')
    except(TypeError):
        messages.error(request, 'Enter your income by going into profile page and update customer')
        return redirect('home')

#############ENDING --> adding new policy inside the users account#############


def CheckingOnApplicant(request,pk): #pk is id of customer
    customer = Applicant.objects.get(id=pk)
    print("Name of the customer using the customer variable, is {}".format(customer))
    #orders = customer.policy_set.all()
    policies_taken_by_applicant = customer.policy_set.all()
    print(policies_taken_by_applicant)
    print("The phone no is {}".format(customer.phone))

    total_policies = policies_taken_by_applicant.count()
    context = {
        'customer': customer,
        'orders': policies_taken_by_applicant,
        'total_orders': total_policies,
        'order_count':total_policies,
    }
    return render(request, 'accounts/policy_admin_pages/checkingOnApplicants.html', context)

# def applying_for_policy_Evaluator(request, pk):#here the pk will be id of policy
#     #I can access the user who is logged in "request.user.applicant"
#     customerWhoIsLoggedIn = request.user.applicant
#     ######## to calculate total existing loan ########
#     ### get the sum of all loan for existing policy
#     setOfPolicyTakenByMember = customerWhoIsLoggedIn.policy_set.all()
#     y = 0
#     for x in setOfPolicyTakenByMember:
#         print(x.loan_amount)
#         y = y + x.loan_amount
#     totalExistingLoanAmount = y
#     ######## to find loan amount to be paid for new policy ########
#     policyCustomerIsChoosing = Policy.objects.get(id=pk)
#     loanAmountOfPolicyChoosen = policyCustomerIsChoosing.loan_amount
#     ######## check if the total loan can be included in the income of the customer ########
#     if customerWhoIsLoggedIn.income > (totalExistingLoanAmount+loanAmountOfPolicyChoosen):
#         print("Approved")
#     else:
#         print("Not Approved")
#     totalExistingLoanAmountAfterNewPolicy=totalExistingLoanAmount+loanAmountOfPolicyChoosen
#     context = {
#         'customerWhoIsLoggedIn': customerWhoIsLoggedIn.id,
#         'policyCustomerIsChoosing': policyCustomerIsChoosing.id,
#         'totalExistingLoanAmount': totalExistingLoanAmount,
#         'totalExistingLoanAmountAfterNewPolicy': totalExistingLoanAmountAfterNewPolicy,
#         'loanAmountOfPolicyChoosen': loanAmountOfPolicyChoosen,

#     }
#     ############## Enitrely new thing
#     return render(request, 'accounts/new.html',context)


'''
Create a function by which if the user clicks on it gets the policy [ie basically add to cart 
functionality in the shopping cart.] checking the capability of this project I found that
in dennisIvy playlist for django he has given the rights to create order to user in part-11
try adding that functionality first.
'''

'''
A function needs to be created wherein it takes the id of the user which is logged in and the 
id of policy on which user wants to apply, then check if the sum of all the existing 'monthly_payment'
and the monthly_payment of the upcoming policiy is greater than income.
'''
