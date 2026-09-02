from django.db import transaction
from django.utils import timezone

from .models import Application, ApplicationCounter


@transaction.atomic
def create_application():
    year = timezone.localdate().year

    counter, created = ApplicationCounter.objects.select_for_update().get_or_create(
        year=year,
        defaults={
            "last_number": 0,
        },
    )

    counter.last_number += 1
    counter.save(update_fields=["last_number"])

    application_number = f"TSC-{year}-{counter.last_number:04d}"

    application = Application.objects.create(
        application_number=application_number,
        status="draft",
    )

    return application