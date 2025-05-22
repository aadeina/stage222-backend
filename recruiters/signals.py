from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from recruiters.models import RecruiterProfile

@receiver(post_save, sender=User)
def create_recruiter_profile(sender, instance, created, **kwargs):
    if created and instance.role == "recruiter":
        if not instance.phone_number:
            # You can also raise an error if preferred
            print("❌ Recruiter created without a phone number.")
            return

        RecruiterProfile.objects.create(
            user=instance,
            phone=instance.phone_number  # ✅ ensure this is passed
        )
