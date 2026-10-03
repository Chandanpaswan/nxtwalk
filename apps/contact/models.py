from django.db import models


class ContactMessage(models.Model):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    CLOSED = "closed"
    STATUS_CHOICES = [
        (NEW, "New"),
        (CONTACTED, "Contacted"),
        (QUALIFIED, "Qualified"),
        (CONVERTED, "Converted"),
        (CLOSED, "Closed"),
    ]
    BUDGET_CHOICES = [
        ("under_100000", "Under INR 1 lakh"),
        ("100000_300000", "INR 1-3 lakh"),
        ("300000_1000000", "INR 3-10 lakh"),
        ("over_1000000", "INR 10 lakh+"),
        ("not_sure", "Not sure yet"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=180, blank=True)
    service = models.ForeignKey("services.Service", on_delete=models.SET_NULL, null=True, blank=True, related_name="contact_messages")
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True)
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField()
    source = models.CharField(max_length=120, default="website")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=NEW, db_index=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"


class ProjectEnquiry(models.Model):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    CLOSED = "closed"
    STATUS_CHOICES = ContactMessage.STATUS_CHOICES

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=180, blank=True)
    service = models.ForeignKey("services.Service", on_delete=models.SET_NULL, null=True, blank=True, related_name="project_enquiries")
    budget = models.CharField(max_length=20, choices=ContactMessage.BUDGET_CHOICES, blank=True)
    timeline = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    source = models.CharField(max_length=120, default="website")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=NEW, db_index=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} project enquiry"
