import uuid
from django.contrib.auth.models import User

from django.db import models


# Create your models here.
# денежная сумма
class Sum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    type = models.BooleanField(default=False) #по умолчанию внесенная сумма всегда считается расходом
    cat = models.ForeignKey('Cat', on_delete=models.PROTECT) #нельзя удалить категорию пока к ней относятся денежные суммы
    week = models.ForeignKey('Week', on_delete=models.PROTECT) #удаление и создание недели вообще не будет предусмотрено api
    date_create = models.DateField(auto_now_add=True)
    last_modified_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.value)

# категория затрат
class Cat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    type = models.BooleanField(default=False) #по умолчанию тип категории всегда относится к расходам
    date_create = models.DateField(auto_now_add=True)
    last_modified_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


# неделя
class Week(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.start_date)

# семья
class Family(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    date_create = models.DateField(auto_now_add=True)
    last_modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.name)

# профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)
