# coding=utf-8
"""Integration tests for the Payrexx webhook -> invoice flow."""

import json
from decimal import Decimal
from unittest import mock

from django.core import mail
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse
from django.utils.translation import override as translation_override

from base.tests.model_factories import ProjectF
from certification.models.invoice import Invoice
from certification.tests.model_factories import (
    CertifyingOrganisationF,
    CreditsOrderF,
)
from core.model_factories import UserF


@override_settings(
    VALID_DOMAIN=['testserver'],
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
)
class PayrexxWebhookInvoiceTest(TestCase):
    def setUp(self):
        self.project = ProjectF.create()
        self.project.credit_cost = Decimal('10.00')
        self.project.credit_cost_currency = 'EUR'
        self.project.invoice_number_prefix = 'QGIS'
        self.project.invoice_issuer_name = 'QGIS.ORG'
        self.project.invoice_issuer_address = 'Issuer street 1'
        self.project.invoice_issuer_email = 'billing@qgis.org'
        self.project.save()
        self.owner = UserF.create(email='owner@example.com')
        self.organisation = CertifyingOrganisationF.create(
            project=self.project,
            name='Webhook Org',
            address='Webhook street',
            organisation_email='org@example.com',
            vat_number='ES-X',
        )
        self.organisation.organisation_owners.add(self.owner)
        self.credits_order = CreditsOrderF.create(
            organisation=self.organisation,
            credits_requested=3,
        )

    def _post_webhook(self):
        payload = {
            'transaction': {
                'id': 'TX-42',
                'referenceId': self.credits_order.pk,
            }
        }
        # Force the URL to use a supported language prefix ('en'); the
        # default LANGUAGE_CODE 'en-us' is not in LANGUAGES so i18n_patterns
        # would resolve it as a 404.
        with translation_override('en'):
            url = reverse('payrexx-webhook')
        return Client().post(
            url,
            data=json.dumps(payload),
            content_type='application/json',
        )

    @mock.patch('certification.views.payrexx.PayrexxService')
    def test_webhook_creates_invoice_and_sends_email(self, mock_service):
        mock_service.return_value.get_transaction.return_value = {
            'status': 'confirmed',
            'referenceId': self.credits_order.pk,
            'id': 'TX-42',
        }

        response = self._post_webhook()
        self.assertEqual(response.status_code, 200)

        invoices = Invoice.objects.filter(credits_order=self.credits_order)
        self.assertEqual(invoices.count(), 1)
        invoice = invoices.get()
        self.assertEqual(invoice.quantity, 3)
        self.assertEqual(invoice.total, Decimal('30.00'))
        self.assertTrue(invoice.pdf)

        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertIn(invoice.invoice_number, sent.subject)
        self.assertIn('owner@example.com', sent.to)
        attachment_names = [att[0] for att in sent.attachments]
        self.assertIn(f'{invoice.invoice_number}.pdf', attachment_names)
        # Email is plain text only — no HTML alternative attached.
        self.assertEqual(getattr(sent, 'alternatives', []), [])

        # Organisation credits incremented.
        self.organisation.refresh_from_db()
        self.assertEqual(self.organisation.organisation_credits, 3)

    @mock.patch('certification.views.payrexx.PayrexxService')
    def test_webhook_replay_is_idempotent(self, mock_service):
        mock_service.return_value.get_transaction.return_value = {
            'status': 'confirmed',
            'referenceId': self.credits_order.pk,
            'id': 'TX-42',
        }

        self._post_webhook()
        # Reset captured outbox to count only the second send (if any).
        mail.outbox = []
        response = self._post_webhook()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Invoice.objects.filter(credits_order=self.credits_order).count(),
            1,
        )
        # No second email — webhook detected credits already issued.
        self.assertEqual(len(mail.outbox), 0)
