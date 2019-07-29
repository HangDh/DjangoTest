from django.db import models, transaction
from django.db.models import F

class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField('Priorytet')
    sendDate = models.DateField('Data wysyłki')

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=100)


class TaskManager(models.Manager):
    def create_task(self, name, order):
        task = self.create(name=name, order=order)

    def move(self, task, new_number):
        qs = self.get_queryset()

        '''transaction.atomic sprawia, że do skończenia operacji nie zostaną dokonane żadne zmiany w bazie danych
        oznacza to, że dopiero na samym końcu będą zapisane, na ostatnim kroku '''
        with transaction.atomic():
            if task.number_ordering > int(new_number):
                qs.filter(
                    order = task.order,
                    number_ordering__lt = task.number_ordering,
                    number_ordering__gte = new_number
                ).exclude(
                    pk = task.pk
                ).update(
                    number_ordering = F('number_ordering') + 1,
                )
            else:
                qs.filter(
                    order = task.order,
                    number_ordering__lte = new_number,
                    number_ordering__gte = task.number_ordering
                ).exclude(
                    pk = task.pk
                ).update(
                    number_ordering = F('number_ordering') - 1,
                )
            
            task.number_ordering = new_number
            task.save()
            
            
class Task(models.Model):
    name = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    objects = TaskManager()
    number_ordering = models.IntegerField(default=1)

    def __str__(self):
        return self.name + ': ' + self.order.name

    class Meta:
        unique_together = ('order', 'name', )