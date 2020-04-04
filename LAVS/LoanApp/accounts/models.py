from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Applicant(models.Model):
    user         = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name         = models.CharField(max_length=200, null=True)
    phone        = models.CharField(max_length=200, null=True)
    email        = models.CharField(max_length=200, null=True)
    CIBIL_score  = models.IntegerField(blank = True, null = True)
    income       = models.IntegerField(blank=True, null=True)
    #date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name

class Policy(models.Model):
    BANK = (
        ('AXIS','AXIS'),
        ('HDFC','HDFC'),
        ('ICICI','ICICI'),
    )
    POLICY_TYPES = (
        ('Home Loan','Home Loan'),
        ('Car Loan', 'Car Loan'),
        ('Educational Loan', 'Educational Loan'),
        ('Personal Loan', 'Personal Loan'),
        ('Buisness Loan', 'Buisness Loan'),
        ('Gold Loan', 'Gold Loan'),
    )
    applicant = models.ForeignKey(Applicant, null=True, on_delete=models.SET_NULL)
    policy_name = models.CharField(max_length=200, null=True, choices=POLICY_TYPES)
    bank = models.CharField(max_length=200, null=True, blank=True, choices=BANK)
    Tenure = models.IntegerField(blank=True, null=True)
    Processing_Fees = models.IntegerField(blank=True, null=True)
    loan_amount = models.IntegerField(blank=True, null=True)
    interest_rate = models.IntegerField(default=5, blank=True, null=True)


    def __str__(self):
        return self.policy_name
