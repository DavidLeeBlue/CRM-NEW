import os
import django

# Set the environment variable to point to your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_main.settings')

# Initialize Django
django.setup()

from ticket.models import TicketImage

# Get all TicketImage entries
images = TicketImage.objects.all()

# Print the file paths of the images
for image in images:
    print(image.image.path)