from django.db import models

# Create your models here.
class Employee(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return self.first_name


class Account(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    password = models.CharField(max_length=97)

    def __str__(self):
        return str(self.employee.id)


class OutstandingToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

    jti = models.CharField(unique=True, max_length=255)

    token = models.CharField(max_length=240)

    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.account} ({self.jti})"


class BlacklistedToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    token = models.OneToOneField(OutstandingToken, on_delete=models.CASCADE)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted token for {self.token.user}"
