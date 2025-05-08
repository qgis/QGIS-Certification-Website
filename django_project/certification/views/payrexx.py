from django.shortcuts import render, redirect
from certification.utilities import PayrexxService
from django.http import HttpResponse
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView

from certification.models.certifying_organisation import CertifyingOrganisation
from base.models.project import Project
from decimal import Decimal
from django.http import Http404
from django.urls import reverse


class PayrexxTopUpView(TemplateView):
  template_name = 'certificate/top_up.html'
  project_slug = ''
  organisation_slug = ''


  def get_context_data(self, **kwargs):
    context = super(PayrexxTopUpView, self).get_context_data(**kwargs)
    self.project_slug = 'qgis'
    self.organisation_slug = self.kwargs.get('organisation_slug', None)

    certifying_organisation = (
        CertifyingOrganisation.objects.get(slug=self.organisation_slug)
    )
    project = Project.objects.get(slug=self.project_slug)

    context['the_project'] = project
    context['cert_organisation'] = certifying_organisation

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

    total_credits = self.request.POST.get('total-credits', None)

    self.project_slug = 'qgis'
    self.organisation_slug = self.kwargs.get('organisation_slug', None)

    project = Project.objects.get(
        slug=self.project_slug
    )

    organisation = CertifyingOrganisation.objects.get(
        slug=self.organisation_slug
    )

    if not total_credits:
        raise Http404('Missing important value')

    try:
      total_credits_decimal = Decimal(total_credits)
      total_credits = int(total_credits)
    except ValueError:
      raise Http404('Wrong total credits format')

    cost_of_credits = project.credit_cost * total_credits_decimal
    description = f"Top up {total_credits} \
      credit{'s' if total_credits > 1 else ''} \
      for {organisation.name}"
    
    payrexx = PayrexxService()
    redirect_url = reverse('payrexx-success')
    response = payrexx.create_gateway(
      amount=cost_of_credits,
      currency=project.credit_cost_currency,
      purpose=description,
      redirect_url=redirect_url,
      firstname=request.user.first_name,
      lastname=request.user.last_name,
      email=request.user.email,
    )
    print('Response:', response)
    if response.get('status') == 'success':
      gateway = response['data'][0]
      return redirect(gateway['link'])
    
    # Handle error
    return render(request, '500.html', {'error': response})

class PayrexxSuccessView(TemplateView):
  template_name = 'certificate/payrexx_success.html'
  project_slug = ''
  organisation_slug = ''

  def get_context_data(self, **kwargs):
    context = super(PayrexxSuccessView, self).get_context_data(**kwargs)
    self.project_slug = 'qgis'
    self.organisation_slug = self.kwargs.get('organisation_slug', None)

    certifying_organisation = (
        CertifyingOrganisation.objects.get(slug=self.organisation_slug)
    )
    project = Project.objects.get(slug=self.project_slug)

    context['the_project'] = project
    context['cert_organisation'] = certifying_organisation

    return context

class PayrexxWebhookView(View):
  def post(self, request, *args, **kwargs):
    """Handle Payrexx webhook notifications

    :param request: HTTP request object
    :type request: HttpRequest

    :param args: Positional arguments
    :type args: tuple

    :param kwargs: Keyword arguments
    :type kwargs: dict

    :returns: Unaltered request object
    :rtype: HttpResponse
    """
    
    # Handle the webhook notification here
    # You can access the data from the request body
    # and process it as needed.
    print('Webhook data:', request.body)

    
    return HttpResponse(status=200)

