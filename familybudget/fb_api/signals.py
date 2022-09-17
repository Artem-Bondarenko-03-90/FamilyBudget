from datetime import date
import datetime
from django.db.models.signals import pre_init
from .models import Sum, Week
from django.dispatch import receiver


# метод создания новой записи Week
@receiver(pre_init, sender=Sum)
def pre_init_dispatcher(sender, **kwargs):
    last_week = Week.objects.all().order_by('start_date').reverse().first()
    while date.today() > last_week.end_date:
        new_week = Week.objects.create(start_date=last_week.end_date + datetime.timedelta(days=1),
                                       end_date=last_week.end_date + datetime.timedelta(weeks=1))
        last_week = Week.objects.all().order_by('start_date').reverse().first()