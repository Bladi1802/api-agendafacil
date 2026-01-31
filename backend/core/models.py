import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ValidationError


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStampedModel):
    class Role(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        BUSINESS = "BUSINESS", "Business"
        ADMIN = "ADMIN", "Admin"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Business(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="businesses")

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=60)
    phone = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="uq_business_owner_name")
        ]

    def __str__(self):
        return f"{self.name} - {self.category}"


class Service(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="services")

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    duration_min = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["business", "name"], name="uq_service_business_name"),
            models.CheckConstraint(check=Q(duration_min__gt=0), name="ck_service_duration_gt_0"),
            models.CheckConstraint(check=Q(price__gte=0), name="ck_service_price_gte_0"),
        ]

    def __str__(self):
        return f"{self.name} ({self.business.name})"


class AvailabilitySlot(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="availability_slots")

    day_of_week = models.PositiveSmallIntegerField()  # 0..6
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(day_of_week__gte=0) & Q(day_of_week__lte=6), name="ck_slot_dow_0_6"),
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("end_time debe ser mayor que start_time.")

    def __str__(self):
        return f"{self.business.name} D{self.day_of_week} {self.start_time}-{self.end_time}"


class Appointment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    business = models.ForeignKey(Business, on_delete=models.PROTECT, related_name="appointments")
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name="appointments")

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.CharField(max_length=250, blank=True)

    services = models.ManyToManyField(Service, through="AppointmentService", related_name="appointments")

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(end_at__gt=models.F("start_at")), name="ck_appointment_end_gt_start"),
        ]

    def __str__(self):
        return f"Cita {self.id} - {self.start_at}"


class AppointmentService(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="appointment_services")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="service_appointments")

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["appointment", "service"], name="uq_appointment_service_once"),
            models.CheckConstraint(check=Q(quantity__gt=0), name="ck_as_quantity_gt_0"),
            models.CheckConstraint(check=Q(unit_price__gte=0), name="ck_as_unit_price_gte_0"),
        ]

    def __str__(self):
        return f"{self.appointment_id} - {self.service.name} x{self.quantity}"
