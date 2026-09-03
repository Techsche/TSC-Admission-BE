from django.contrib import admin
from django.apps import apps


app_config = apps.get_app_config("admissions")

for model in app_config.get_models():
    if model not in admin.site._registry:
        admin.site.register(model)