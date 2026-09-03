import hashlib
import secrets

from django.db import transaction
from django.utils import timezone

from .models import Application


def create_application():
    with transaction.atomic():

        year = timezone.now().year

        # Generate a secure random access token
        access_token = secrets.token_urlsafe(32)

        # Hash token before storing it
        access_token_hash = hashlib.sha256(
            access_token.encode("utf-8")
        ).hexdigest()

        # Generate application number
        last_application = (
            Application.objects
            .filter(application_number__startswith=f"TSC-{year}-")
            .order_by("-application_number")
            .first()
        )

        if last_application:
            last_number = int(
                last_application.application_number.split("-")[-1]
            )
            next_number = last_number + 1
        else:
            next_number = 1

        application_number = f"TSC-{year}-{next_number:04d}"

        application = Application.objects.create(
            application_number=application_number,
            status="draft",
            access_token_hash=access_token_hash,
        )

        return application, access_token