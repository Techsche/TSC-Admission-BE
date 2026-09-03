import uuid
import hashlib
import secrets
from django.db import models
from django.contrib.auth.models import User


class ApplicationCounter(models.Model):

    year = models.PositiveIntegerField(
        unique=True
    )

    last_number = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.year} - {self.last_number}"


class Application(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("under_review", "Under Review"),
        ("admitted", "Admitted"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    application_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )
    
    access_token_hash = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        db_index=True,
        null=True,
        blank=True,
    )

    # Student Details
    full_name = models.CharField(
        max_length=150,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    mobile = models.CharField(
        max_length=15,
        blank=True,
    )

    # Father Details
    father_name = models.CharField(
        max_length=150,
        blank=True,
    )

    father_mobile = models.CharField(
        max_length=15,
        blank=True,
    )

    # Mother Details
    mother_name = models.CharField(
        max_length=150,
        blank=True,
    )

    mother_mobile = models.CharField(
        max_length=15,
        blank=True,
    )

    # Application Status
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True,
    )

    profile_completed = models.BooleanField(
        default=False,
    )

    declaration_accepted = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.application_number} - {self.full_name}"
    
    
# =============================================================
# CURRENT ADDRESS
# =============================================================

class CurrentAddress(models.Model):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="current_address",
    )

    address_line1 = models.CharField(
        max_length=255,
        blank=True,
    )

    address_line2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    district = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
    )

    def __str__(self):
        return f"{self.application.application_number} - Current Address"


# =============================================================
# PERMANENT ADDRESS
# =============================================================

class PermanentAddress(models.Model):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="permanent_address",
    )

    address_line1 = models.CharField(
        max_length=255,
        blank=True,
    )

    address_line2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    district = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
    )

    def __str__(self):
        return f"{self.application.application_number} - Permanent Address"

    
    
class EducationalQualification(models.Model):
    qualification = models.CharField(max_length=100)
    
    def __str__(self):
        return self.qualification  
    
class Education(models.Model):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="education",
    )

    highest_qualification = models.ForeignKey(
        EducationalQualification, 
        on_delete=models.PROTECT
    )

    def __str__(self):
        return (
            f"{self.application.application_number} - "
            f"{self.highest_qualification.qualification}"
        )


class Document(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ("qualification", "Highest Qualification Certificate"),
        ("aadhaar", "Aadhaar"),
        ("photo", "Photo"),
        ("signature", "Signature"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES,
    )

    file = models.FileField(
        upload_to="admissions/documents/%Y/%m/",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["application", "document_type"],
                name="unique_application_document_type",
            )
        ]

    def __str__(self):
        return (
            f"{self.application.application_number} - "
            f"{self.get_document_type_display()}"
        )