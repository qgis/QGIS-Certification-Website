from django.db import models
from .certifying_organisation import CertifyingOrganisation


class CreditsOrder(models.Model):
  organisation = models.ForeignKey(
    CertifyingOrganisation,
    on_delete=models.CASCADE,
    related_name='credits_orders',
    help_text="The certifying organisation that placed the order"
  )
  credits_requested = models.IntegerField(help_text="Number of credits requested in the order")
  credits_issued = models.BooleanField(default=False, help_text="Flag to indicate if credits have been issued")
  created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the payment was created")
  updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the payment was last updated")
