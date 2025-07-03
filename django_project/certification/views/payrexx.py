import json
import logging
from decimal import Decimal

from base.models.project import Project
from certification.mixins import ActiveCertifyingOrganisationRequiredMixin
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.models.credits_order import CreditsOrder
from certification.utilities import PayrexxService
from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class PayrexxTopUpView(ActiveCertifyingOrganisationRequiredMixin, TemplateView):
    template_name = "certificate/top_up.html"
    project_slug = ""
    organisation_slug = ""

    def get_context_data(self, **kwargs):
        context = super(PayrexxTopUpView, self).get_context_data(**kwargs)
        self.project_slug = "qgis"
        self.organisation_slug = self.kwargs.get("organisation_slug", None)

        certifying_organisation = CertifyingOrganisation.objects.get(
            slug=self.organisation_slug
        )
        project = Project.objects.get(slug=self.project_slug)

        context["the_project"] = project
        context["cert_organisation"] = certifying_organisation

        return context

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        total_credits = self.request.POST.get("total-credits", None)

        self.project_slug = "qgis"
        self.organisation_slug = self.kwargs.get("organisation_slug", None)

        project = Project.objects.get(slug=self.project_slug)

        organisation = CertifyingOrganisation.objects.get(slug=self.organisation_slug)

        if not total_credits:
            raise Http404("Missing important value")

        try:
            total_credits_decimal = Decimal(total_credits)
            total_credits = int(total_credits)
        except ValueError:
            raise Http404("Wrong total credits format")

        cost_of_credits = project.credit_cost * total_credits_decimal
        description = f"Top up {total_credits} \
      credit{'s' if total_credits > 1 else ''} \
      for {organisation.name}"

        payrexx = PayrexxService()

        # Create a new CreditsOrder instance
        credits_order = CreditsOrder.objects.create(
            organisation=organisation,
            credits_requested=total_credits,
        )

        redirect_url = reverse(
            "certifyingorganisation-detail", kwargs={"slug": self.organisation_slug}
        )
        response = payrexx.create_gateway(
            reference_id=credits_order.pk,
            amount=cost_of_credits,
            currency=project.credit_cost_currency,
            purpose=description,
            redirect_url=redirect_url,
            firstname=request.user.first_name,
            lastname=request.user.last_name,
            email=request.user.email,
        )
        if response.get("status") == "success":
            gateway = response["data"][0]
            return redirect(gateway["link"])
        else:
            credits_order.delete()

        # Handle error
        return render(request, "500.html", {"error": response})


@method_decorator(csrf_exempt, name="dispatch")  # disable CSRF for webhooks
class PayrexxWebhookView(View):

    def post(self, request, *args, **kwargs):
        # Step 1: Get POST data
        try:
            payload = json.loads(request.body)  # Parse JSON data from request body
        except json.JSONDecodeError:
            return HttpResponseForbidden("Invalid JSON")

        # Step 2: Verify the transaction
        transaction = payload.get("transaction", None)
        transaction_id = transaction.get("id", None) if transaction else None
        reference_id = transaction.get("referenceId", None) if transaction else None
        if not transaction or not transaction_id or not reference_id:
            return HttpResponse(
                "Webhook triggered with non-credits order data. No action taken.",
                status=200,
            )

        # Step 3: Get the CreditsOrder instance
        get_object_or_404(CreditsOrder, pk=int(reference_id))

        try:
            payrexx = PayrexxService()
            verified_transation = payrexx.get_transaction(transaction_id)
            if verified_transation.get("status") != "confirmed":
                return HttpResponse(
                    "Transaction not confirmed! No credits issued.", status=200
                )
        except Exception:
            return HttpResponseForbidden("Transaction not found!")

        verified_reference_id = verified_transation.get("referenceId", None)
        # Step 4: Update the organization's credits
        credits_order = get_object_or_404(CreditsOrder, pk=int(verified_reference_id))
        if credits_order.credits_issued:
            return HttpResponse("Credits already issued. No action taken.", status=200)
        organisation = credits_order.organisation
        current_credits = organisation.organisation_credits or 0
        organisation.organisation_credits = (
            current_credits + credits_order.credits_requested
        )
        organisation.save()
        credits_order.credits_issued = True
        credits_order.save()

        # Step 5: Send email to organisation owners
        organisation_owners = organisation.organisation_owners.all()
        send_mail(
            subject=f"QGIS Certification: Credits Top Up for {organisation.name}",
            message=f"Your organisation has been credited with {credits_order.credits_requested} credits.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner.email for owner in organisation_owners],
        )

        # Step 6: Respond 200 OK
        return HttpResponse("Credits updated with success!", status=200)
