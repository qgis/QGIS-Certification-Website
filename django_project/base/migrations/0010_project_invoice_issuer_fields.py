# Generated for issue #101 (automated invoice sending)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0009_remove_project_changelog_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="invoice_issuer_name",
            field=models.CharField(
                blank=True,
                default="QGIS.ORG",
                help_text=(
                    "Issuer (seller) name displayed on credit purchase "
                    "invoices."
                ),
                max_length=200,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="invoice_issuer_address",
            field=models.TextField(
                blank=True,
                default="Via Geinas 2\nCH-7031 Laax",
                help_text=(
                    "Issuer postal address displayed on credit purchase "
                    "invoices."
                ),
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="invoice_issuer_vat",
            field=models.CharField(
                blank=True,
                default="UID-Nr: CHE-489.853.176",
                help_text=(
                    "Issuer VAT or company registration number "
                    "(rendered as e.g. 'UID-Nr: CHE-…')."
                ),
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="invoice_issuer_email",
            field=models.EmailField(
                blank=True,
                default="finance@qgis.org",
                help_text="Issuer contact email displayed on invoices.",
                max_length=254,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="invoice_issuer_phone",
            field=models.CharField(
                blank=True,
                default="Mobile: +41 79 938 11 71",
                help_text="Issuer contact phone displayed on invoices.",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="invoice_issuer_bank_details",
            field=models.TextField(
                blank=True,
                default=(
                    "Bank name and address:\n\n"
                    "PostFinance AG\n"
                    "Mingerstrasse 20\n"
                    "3030 Berne\n"
                    "Switzerland\n\n"
                    "Account Name: QGIS.ORG Association\n"
                    "Account Holder Address: Via Geinas 2, CH-7031 Laax, "
                    "Switzerland\n"
                    "IBAN (account nr): CH09 0900 0000 9146 3839 8\n"
                    "BIC/SWIFT: POFICHBEXXX"
                ),
                help_text=(
                    "Issuer bank details / IBAN / SWIFT shown in invoice "
                    "footer."
                ),
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="invoice_number_prefix",
            field=models.CharField(
                blank=True,
                default="QGIS-Cert",
                help_text=(
                    "Prefix used in invoice numbers, e.g. 'QGIS-Cert' -> "
                    "'QGIS-Cert-26-0001'."
                ),
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="invoice_tax_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text=(
                    "Tax / VAT percentage applied to invoices. Leave blank "
                    "for no tax line."
                ),
                max_digits=5,
                null=True,
            ),
        ),
    ]
