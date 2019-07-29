from django.contrib import admin

from ChainTest.models import Country, City, Person, Order, Task

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Person)
admin.site.register(Order)
admin.site.register(Task)