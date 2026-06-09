# Generated for issue #101 (automated invoice sending)

from decimal import Decimal

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("certification", "0029_creditsorder"),
    ]

    operations = [
        migrations.AddField(
            model_name="certifyingorganisation",
            name="vat_number",
            field=models.CharField(
                blank=True,
                help_text=(
                    "VAT or company registration number "
                    "(optional, shown on invoices)."
                ),
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalcertifyingorganisation",
            name="vat_number",
            field=models.CharField(
                blank=True,
                help_text=(
                    "VAT or company registration number "
                    "(optional, shown on invoices)."
                ),
                max_length=50,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("invoice_number", models.CharField(max_length=50, unique=True)),
                ("issue_date", models.DateField(auto_now_add=True)),
                ("billing_name", models.CharField(max_length=200)),
                ("billing_address", models.TextField()),
                (
                    "billing_email",
                    models.CharField(blank=True, default="", max_length=200),
                ),
                (
                    "billing_vat_number",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                (
                    "billing_country",
                    django_countries.fields.CountryField(blank=True, max_length=2),
                ),
                (
                    "issuer_name",
                    models.CharField(blank=True, default="", max_length=200),
                ),
                ("issuer_address", models.TextField(blank=True, default="")),
                (
                    "issuer_vat",
                    models.CharField(blank=True, default="", max_length=100),
                ),
                (
                    "issuer_email",
                    models.CharField(blank=True, default="", max_length=200),
                ),
                (
                    "issuer_phone",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                (
                    "issuer_url",
                    models.URLField(blank=True, default="", max_length=200),
                ),
                ("issuer_bank_details", models.TextField(blank=True, default="")),
                (
                    "quantity",
                    models.IntegerField(help_text="Number of credits purchased."),
                ),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(max_length=10)),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "tax_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "tax_amount",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=12
                    ),
                ),
                ("total", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "payment_reference",
                    models.CharField(blank=True, default="", max_length=100),
                ),
                (
                    "pdf",
                    models.FileField(blank=True, upload_to="invoices/%Y/%m/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "credits_order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="invoice",
                        to="certification.creditsorder",
                    ),
                ),
            ],
            options={
                "ordering": ["-issue_date", "-id"],
            },
        ),
    ]
