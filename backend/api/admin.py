from django.contrib import admin
from .models import Business, Service, Customer, Appointment

# Register your models here.

admin.site.register(Business)
admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(Appointment)
