import random
import string
from core.models import SignupPin

def generate_unique_pin(length=10):
    """Generate a unique PIN."""
    while True:
        pin = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits, k=length
            )
        )
        if not SignupPin.objects.filter(pin=pin).exists():
            return pin
