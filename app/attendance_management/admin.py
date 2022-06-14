from django.contrib import admin
from .models import Employee, Account, OutstandingToken

# Register your models here.

admin.site.register(Employee)
admin.site.register(Account)

admin.site.register(OutstandingToken)
