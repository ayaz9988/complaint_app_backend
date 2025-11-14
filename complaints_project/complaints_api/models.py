from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    # The user who filed the complaint; optional for anonymous complaints or can be required
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    
    # Basic details of the complaint
    title = models.CharField(max_length=255, help_text="Brief summary of the complaint")
    description = models.TextField(help_text="Detailed description of the complaint")
    
    # Optional category or type of complaint, e.g., product, service, billing
    category = models.CharField(max_length=100, blank=True, null=True)
    
    # Priority level to help triage complaints
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Status to indicate the current state of complaint resolution
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Date and time fields to track complaint lifecycle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True, help_text="When the complaint was resolved")

    # Optional contact information to reach out to the complainant
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)

    # Allow attaching related evidence or documents
    attachment = models.FileField(upload_to='complaint_attachments/', null=True, blank=True)

    # Flag for internal usage, e.g., whether this is a flagged or escalated complaint
    escalated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} [{self.status}]"
