# coding=utf-8
"""Tests for Invoice.generate_number."""

from datetime import date
from unittest import mock

from django.test import TestCase

from base.tests.model_factories import ProjectF
from certification.models.invoice import Invoice
from certification.tests.model_factories import (
    CertifyingOrganisationF,
    CreditsOrderF,
    InvoiceF,
)


class InvoiceNumberGenerationTest(TestCase):
    def setUp(self):
        self.project = ProjectF.create(invoice_number_prefix='QGIS-Cert')
        self.project.invoice_number_prefix = 'QGIS-Cert'
        self.project.save()
        self.organisation = CertifyingOrganisationF.create(project=self.project)

    def _make_order(self):
        return CreditsOrderF.create(organisation=self.organisation)

    def test_first_number_uses_prefix_and_year(self):
        with mock.patch(
            'certification.models.invoice.timezone.now',
            return_value=mock.Mock(year=2026),
        ):
            number = Invoice.generate_number(self.project)
        self.assertTrue(number.startswith('QGIS-Cert-26-'))
        self.assertTrue(number.endswith('-0001'))

    def test_sequence_increments_per_year(self):
        InvoiceF.create(
            credits_order=self._make_order(),
            invoice_number='QGIS-Cert-26-0001',
        )
        InvoiceF.create(
            credits_order=self._make_order(),
            invoice_number='QGIS-Cert-26-0002',
        )
        with mock.patch(
            'certification.models.invoice.timezone.now',
            return_value=mock.Mock(year=2026),
        ):
            number = Invoice.generate_number(self.project)
        self.assertEqual(number, 'QGIS-Cert-26-0003')

    def test_falls_back_to_default_prefix_when_blank(self):
        self.project.invoice_number_prefix = ''
        self.project.save()
        with mock.patch(
            'certification.models.invoice.timezone.now',
            return_value=mock.Mock(year=2026),
        ):
            number = Invoice.generate_number(self.project)
        self.assertTrue(number.startswith('QGIS-Cert-26-'))

    def test_year_resets_sequence(self):
        InvoiceF.create(
            credits_order=self._make_order(),
            invoice_number='QGIS-Cert-25-0009',
        )
        with mock.patch(
            'certification.models.invoice.timezone.now',
            return_value=mock.Mock(year=2026),
        ):
            number = Invoice.generate_number(self.project)
        self.assertEqual(number, 'QGIS-Cert-26-0001')

    def test_persisted_invoice_uses_today_date(self):
        invoice = InvoiceF.create(credits_order=self._make_order())
        self.assertEqual(invoice.issue_date, date.today())
