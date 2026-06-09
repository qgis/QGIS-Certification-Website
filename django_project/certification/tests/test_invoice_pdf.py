# coding=utf-8
"""Tests for invoice PDF rendering."""

from decimal import Decimal

from django.test import TestCase

from base.tests.model_factories import ProjectF
from certification.invoice_utils import (
    create_and_send_invoice,
    render_invoice_pdf,
)
from certification.models.invoice import Invoice
from certification.tests.model_factories import (
    CertifyingOrganisationF,
    CreditsOrderF,
    InvoiceF,
)


class InvoicePdfRenderTest(TestCase):
    def setUp(self):
        self.project = ProjectF.create()
        self.organisation = CertifyingOrganisationF.create(project=self.project)
        self.credits_order = CreditsOrderF.create(organisation=self.organisation)

    def test_render_returns_pdf_bytes(self):
        invoice = InvoiceF.create(credits_order=self.credits_order)
        pdf_bytes = render_invoice_pdf(invoice)
        self.assertIsInstance(pdf_bytes, (bytes, bytearray))
        self.assertGreater(len(pdf_bytes), 0)
        self.assertTrue(pdf_bytes.startswith(b'%PDF'))


class CreateAndSendInvoiceTest(TestCase):
    def setUp(self):
        # ProjectF.create dedupes by name; set invoice fields after fetch.
        self.project = ProjectF.create()
        self.project.credit_cost = Decimal('10.00')
        self.project.credit_cost_currency = 'EUR'
        self.project.invoice_number_prefix = 'QGIS'
        self.project.invoice_issuer_name = 'QGIS.ORG'
        self.project.invoice_issuer_address = 'Issuer street 1\n1234 City'
        self.project.save()
        self.organisation = CertifyingOrganisationF.create(
            project=self.project,
            name='Test Org',
            address='Org street 2',
            organisation_email='org@example.com',
            vat_number='ES-B12345678',
        )
        self.credits_order = CreditsOrderF.create(
            organisation=self.organisation,
            credits_requested=7,
        )

    def test_creates_invoice_with_billing_snapshot(self):
        invoice = create_and_send_invoice(
            self.credits_order, payrexx_transaction={'id': 'TX-1'})
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.billing_name, 'Test Org')
        self.assertEqual(invoice.billing_vat_number, 'ES-B12345678')
        self.assertEqual(invoice.issuer_name, 'QGIS.ORG')
        self.assertEqual(invoice.quantity, 7)
        self.assertEqual(invoice.unit_price, Decimal('10.00'))
        self.assertEqual(invoice.subtotal, Decimal('70.00'))
        self.assertEqual(invoice.total, Decimal('70.00'))
        self.assertEqual(invoice.currency, 'EUR')
        self.assertEqual(invoice.payment_reference, 'TX-1')
        self.assertTrue(invoice.invoice_number.startswith('QGIS-'))
        self.assertTrue(invoice.pdf)

    def test_applies_tax_rate(self):
        self.project.invoice_tax_rate = Decimal('21.00')
        self.project.save()
        invoice = create_and_send_invoice(self.credits_order)
        self.assertEqual(invoice.subtotal, Decimal('70.00'))
        self.assertEqual(invoice.tax_amount, Decimal('14.70'))
        self.assertEqual(invoice.total, Decimal('84.70'))

    def test_is_idempotent(self):
        first = create_and_send_invoice(self.credits_order)
        second = create_and_send_invoice(self.credits_order)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(Invoice.objects.filter(
            credits_order=self.credits_order).count(), 1)
