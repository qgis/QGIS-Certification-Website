# coding=utf-8
"""Invoice creation, PDF rendering and email delivery."""

import ast
import logging
import os
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, get_connection
from django.db import transaction
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _quantize(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def render_invoice_pdf(invoice) -> bytes:
    """Render the invoice as a PDF using WeasyPrint."""
    from weasyprint import HTML  # imported lazily — weasyprint loads native libs

    project = invoice.credits_order.organisation.project
    logo_url = ''
    if project.image_file:
        try:
            logo_url = project.image_file.path
        except (ValueError, NotImplementedError):
            logo_url = project.image_file.url

    html = render_to_string(
        'invoice/invoice.html',
        {'invoice': invoice, 'logo_url': logo_url},
    )
    return HTML(string=html, base_url=settings.MEDIA_ROOT).write_pdf()


def send_invoice_email(invoice) -> None:
    """Email the invoice (PDF attached) to organisation owners."""
    organisation = invoice.credits_order.organisation
    recipients = {
        owner.email for owner in organisation.organisation_owners.all() if owner.email
    }
    if organisation.organisation_email:
        recipients.add(organisation.organisation_email)
    if not recipients:
        logger.warning(
            "No recipients found for invoice %s — email skipped.",
            invoice.invoice_number,
        )
        return

    connection = None
    if settings.DEBUG:
        # Reroute every dev invoice to the dev team and force a real SMTP
        # connection — the dev EMAIL_BACKEND is the console backend, which
        # would otherwise dump the full MIME (incl. the base64 PDF) into the
        # logs and never actually deliver the email. SMTP credentials are
        # pulled from env vars (the dev settings hardcode EMAIL_HOST to
        # localhost, which would refuse the connection).
        logger.info(
            "DEBUG mode: redirecting invoice %s email from %s to the dev team.",
            invoice.invoice_number,
            sorted(recipients),
        )
        recipients = os.environ.get('ADMIN_EMAIL', '').split(',')
        try:
            use_tls = ast.literal_eval(os.environ.get('EMAIL_USE_TLS', 'True'))
        except (ValueError, SyntaxError):
            use_tls = True
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=os.environ.get('EMAIL_HOST', 'smtp.resend.com'),
            port=int(os.environ.get('EMAIL_PORT', '587') or 587),
            username=os.environ.get('EMAIL_HOST_USER') or None,
            password=os.environ.get('EMAIL_HOST_PASSWORD') or None,
            use_tls=bool(use_tls),
        )

    ctx = {'invoice': invoice, 'organisation': organisation}
    subject = f"QGIS Certification: Invoice {invoice.invoice_number}"
    text_body = render_to_string('email/invoice_email.txt', ctx)

    msg = EmailMessage(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=sorted(recipients),
        connection=connection,
    )
    if invoice.pdf:
        invoice.pdf.open('rb')
        try:
            pdf_bytes = invoice.pdf.read()
        finally:
            invoice.pdf.close()
        msg.attach(f"{invoice.invoice_number}.pdf", pdf_bytes, 'application/pdf')
    msg.send()


def create_and_send_invoice(credits_order, payrexx_transaction=None):
    """Create an Invoice record for a paid CreditsOrder and email it.

    Idempotent: re-invocation for the same CreditsOrder is a no-op so the
    Payrexx webhook can safely retry. PDF rendering / email failures are
    logged but never raise — the credits have already been issued and we do
    not want to fail the webhook.
    """
    from certification.models.invoice import Invoice

    organisation = credits_order.organisation
    project = organisation.project

    with transaction.atomic():
        existing = (
            Invoice.objects
            .select_for_update()
            .filter(credits_order=credits_order)
            .first()
        )
        if existing:
            logger.info(
                "Invoice %s already exists for credits order %s — skipping.",
                existing.invoice_number,
                credits_order.pk,
            )
            return existing

        quantity = credits_order.credits_requested
        unit_price = Decimal(project.credit_cost or 0)
        subtotal = _quantize(unit_price * Decimal(quantity))
        tax_rate = project.invoice_tax_rate
        if tax_rate is not None:
            tax_amount = _quantize(subtotal * Decimal(tax_rate) / Decimal('100'))
        else:
            tax_amount = Decimal('0.00')
        total = _quantize(subtotal + tax_amount)

        payment_reference = ''
        if payrexx_transaction:
            payment_reference = str(payrexx_transaction.get('id', '')) or ''

        invoice = Invoice.objects.create(
            credits_order=credits_order,
            invoice_number=Invoice.generate_number(project),
            billing_name=organisation.name,
            billing_address=organisation.address or '',
            billing_email=organisation.organisation_email or '',
            billing_vat_number=organisation.vat_number or '',
            billing_country=organisation.country or '',
            issuer_name=project.invoice_issuer_name or '',
            issuer_address=project.invoice_issuer_address or '',
            issuer_vat=project.invoice_issuer_vat or '',
            issuer_email=project.invoice_issuer_email or '',
            issuer_phone=project.invoice_issuer_phone or '',
            issuer_url=project.project_url or '',
            issuer_bank_details=project.invoice_issuer_bank_details or '',
            quantity=quantity,
            unit_price=unit_price,
            currency=project.credit_cost_currency or '',
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total=total,
            payment_reference=payment_reference,
        )

    # PDF + email outside the DB transaction so a render/send failure does
    # not roll back the persisted Invoice (we want the record kept either way).
    try:
        pdf_bytes = render_invoice_pdf(invoice)
        invoice.pdf.save(
            f"{invoice.invoice_number}.pdf",
            ContentFile(pdf_bytes),
            save=True,
        )
    except Exception:
        logger.exception(
            "Failed to render PDF for invoice %s", invoice.invoice_number)

    try:
        send_invoice_email(invoice)
    except Exception:
        logger.exception(
            "Failed to send invoice email for %s", invoice.invoice_number)

    return invoice
