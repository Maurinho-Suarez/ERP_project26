from django.db import models
from django.conf import settings
from core.models import Status, Country, Currency

class AccountNature(models.Model):
    id_accounting_nature = models.CharField(verbose_name="Accounting Nature ID", max_length=10, primary_key=True)
    name = models.CharField(verbose_name="Name", max_length=50)
    symbol = models.TextField(verbose_name="Symbol", blank=True)
    effect_on_balance = models.TextField(verbose_name="Effect on Balance")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Accounting Nature"
        verbose_name_plural = "Accounting Natures"

    def __str__(self):
        return self.name


class AccountGroup(models.Model):
    id_account_group = models.CharField(verbose_name="Account Group ID", max_length=10, primary_key=True)
    name = models.CharField(verbose_name="Name", max_length=50)
    code_prefix = models.CharField(verbose_name="Code Prefix", max_length=10)
    description = models.TextField(verbose_name="Description", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Account Group"
        verbose_name_plural = "Account Groups"

    def __str__(self):
        return self.name


class AccountType(models.Model):
    id_account_type = models.CharField(verbose_name="Account Type ID", max_length=10, primary_key=True)
    name = models.CharField(verbose_name="Name", max_length=50)
    description = models.TextField(verbose_name="Description", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Account Type"
        verbose_name_plural = "Account Types"

    def __str__(self):
        return self.name

class AccountAccount(models.Model):
    id_account = models.CharField(verbose_name="Account ID", max_length=10, primary_key=True)
    name = models.CharField(verbose_name="Name", max_length=50)
    code = models.CharField(verbose_name="Code", max_length=20)
    description = models.TextField(verbose_name="Description", blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, verbose_name="Account Type")
    account_group = models.ForeignKey(AccountGroup, on_delete=models.PROTECT, verbose_name="Account Group")
    nature = models.ForeignKey(AccountNature, on_delete=models.PROTECT, verbose_name="Accounting Nature")
    currency_id = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Currency")
    country_id = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="Country")
    is_control_account = models.BooleanField(default=False, verbose_name="Is Control Account")
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Parent Account")

    status = models.ForeignKey(Status, default=1, on_delete=models.PROTECT, verbose_name="Status")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.code} - {self.name}"