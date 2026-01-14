from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    """Customer model for CRM module"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    lead_source = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('customer', 'Customer'),
        ('inactive', 'Inactive'),
    ], default='lead')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Lead(models.Model):
    """Lead model for tracking potential customers"""
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    probability = models.IntegerField(default=0)
    expected_close_date = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ], default='new')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.customer}"

class Contact(models.Model):
    """Contact model for customer interactions"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField(max_length=20, choices=[
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
    ], default='note')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    contact_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact_type} - {self.customer}"
