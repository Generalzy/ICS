from django.test import TestCase
import os
from django.db.models import Max, Min, Count, Sum, Avg

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ICS.settings")
    import django

    django.setup()
    from app01 import models

    commodity_query = models.Commodity.objects.all()
    print(commodity_query)
    for com in commodity_query:
        print(com.factory.all())