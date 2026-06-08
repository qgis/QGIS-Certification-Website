# coding=utf-8
"""Invoice model for credit purchases."""

from datetime import timedelta
from decimal import Decimal

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from certification.models.credits_order import CreditsOrder


CURRENCY_SYMBOLS = {
    'EUR': '€',
    'USD': '$',
    'GBP': '£',
    'CHF': 'CHF',
}


class Invoice(models.Model):
    """Invoice issued when an organisation buys credits.

    Holds a frozen snapshot of billing and issuer data so historical
    invoices stay correct even when the underlying records change later.
    """

    credits_order = models.OneToOneField(
        CreditsOrder,
        on_delete=models.PROTECT,
        related_name='invoice',
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField(auto_now_add=True)

    # Billing snapshot
    billing_name = models.CharField(max_length=200)
    billing_address = models.TextField()
    billing_email = models.CharField(max_length=200, blank=True, default="")
    billing_vat_number = models.CharField(max_length=50, blank=True, default="")
    billing_country = CountryField(blank=True)

    # Issuer snapshot
    issuer_name = models.CharField(max_length=200, blank=True, default="")
    issuer_address = models.TextField(blank=True, default="")
    issuer_vat = models.CharField(max_length=100, blank=True, default="")
    issuer_email = models.CharField(max_length=200, blank=True, default="")
    issuer_phone = models.CharField(max_length=50, blank=True, default="")
    issuer_url = models.URLField(max_length=200, blank=True, default="")
    issuer_bank_details = models.TextField(blank=True, default="")

    # Amounts
    quantity = models.IntegerField(help_text=_("Number of credits purchased."))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=12, decimal_places=2)

    payment_reference = models.CharField(max_length=100, blank=True, default="")
    pdf = models.FileField(upload_to='invoices/%Y/%m/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'certification'
        ordering = ['-issue_date', '-id']

    def __str__(self):
        return self.invoice_number

    @property
    def due_date(self):
        """Default payment due date — 30 days after issue."""
        return self.issue_date + timedelta(days=30)

    @property
    def currency_symbol(self):
        return CURRENCY_SYMBOLS.get(self.currency.upper(), self.currency)

    @classmethod
    def generate_number(cls, project):
        """Return the next sequential invoice number for the given project.

        Format: ``{PREFIX}-{YYYY}-{NNNN}``. Uses ``select_for_update`` so two
        concurrent callers cannot allocate the same number.
        """
        prefix = (project.invoice_number_prefix or 'INV').strip()
        year = timezone.now().year
        search_prefix = f'{prefix}-{year}-'

        with transaction.atomic():
            last = (
                cls.objects
                .select_for_update()
                .filter(invoice_number__startswith=search_prefix)
                .order_by('-invoice_number')
                .first()
            )
            if last:
                try:
                    last_seq = int(last.invoice_number.rsplit('-', 1)[-1])
                except ValueError:
                    last_seq = 0
            else:
                last_seq = 0
            return f'{search_prefix}{last_seq + 1:04d}'
