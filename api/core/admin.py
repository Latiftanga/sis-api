from django.contrib import admin

# Register your models here.
from django.contrib import admin
from core.models import SignupPin
from core.utils import generate_unique_pin


class SignupPinAdmin(admin.ModelAdmin):
    list_display = ('pin', 'is_used', 'created_at', 'user')

    def generate_pins(self, request, queryset):
        # Generate and save new PINs
        for _ in range(10):  # Example: Generate 10 new PINs
            pin = generate_unique_pin()
            SignupPin.objects.create(pin=pin)

    actions = [generate_pins]

admin.site.register(SignupPin, SignupPinAdmin)
