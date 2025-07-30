# coding=utf-8
from base.models import Project
from braces.views import LoginRequiredMixin
from certification.mixins import ActiveCertifyingOrganisationRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from ..forms import TrainingCenterForm
from ..models import CertifyingOrganisation, TrainingCenter


class TrainingCenterMixin(object):
    """Mixin class to provide standard settings for Training Center."""

    model = TrainingCenter
    form_class = TrainingCenterForm


# noinspection PyAttributeOutsideInit.
class TrainingCenterCreateView(
    LoginRequiredMixin,
    ActiveCertifyingOrganisationRequiredMixin,
    TrainingCenterMixin,
    CreateView,
):
    """Create view for Training Center."""

    context_object_name = "trainingcenter"
    template_name = "training_center/create.html"

    def get_success_url(self):
        """Define the redirect URL.

         After successful creation of the object, the User will be redirected
         to the Certifying Organisation detail page
         for the object's parent Certifying Organisation.

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse(
            "certifyingorganisation-detail",
            kwargs={
                "slug": self.object.certifying_organisation.slug,
            },
        )

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(TrainingCenterCreateView, self).get_context_data(**kwargs)
        context["trainingcenters"] = self.get_queryset().filter(
            certifying_organisation=self.certifying_organisation
        )
        context["organisation"] = self.certifying_organisation
        return context

    def form_valid(self, form):
        """Save new created Training Center.

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""
        try:
            super(TrainingCenterCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                "ERROR: Training Center by this name is already exists!"
            )

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(TrainingCenterCreateView, self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get("organisation_slug", None)
        self.certifying_organisation = CertifyingOrganisation.objects.get(
            slug=self.organisation_slug
        )
        kwargs.update(
            {
                "user": self.request.user,
                "certifying_organisation": self.certifying_organisation,
            }
        )
        return kwargs


class TrainingCenterDetailView(
    ActiveCertifyingOrganisationRequiredMixin, TrainingCenterMixin, DetailView
):
    """Detail view for Training Center."""

    context_object_name = "trainingcenter"
    template_name = "training_center/detail.html"

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.organisation_slug = self.kwargs.get("organisation_slug", None)
        self.certifying_organisation = CertifyingOrganisation.objects.get(
            slug=self.organisation_slug
        )
        context = super(TrainingCenterDetailView, self).get_context_data(**kwargs)
        context["trainingcenters"] = TrainingCenter.objects.filter(
            certifying_organisation=self.certifying_organisation
        )
        project_slug = "qgis"
        context["project_slug"] = project_slug
        if project_slug:
            context["the_project"] = Project.objects.get(slug=project_slug)
            context["project"] = context["the_project"]
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all training center in the
            corresponding organisation.
        :rtype: QuerySet
        """

        qs = TrainingCenter.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a training center
            within the organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get("slug", None)
            organisation_slug = self.kwargs.get("organisation_slug", None)
            if slug and organisation_slug:
                certifying_organisation = CertifyingOrganisation.objects.get(
                    slug=organisation_slug
                )
                obj = queryset.get(
                    certifying_organisation=certifying_organisation, slug=slug
                )
                return obj
            else:
                raise Http404("Sorry! We could not find " "your training centers!")


class TrainingCenterDeleteView(
    LoginRequiredMixin, ActiveCertifyingOrganisationRequiredMixin, DeleteView
):
    """Delete view for Training Center."""

    model = TrainingCenter
    context_object_name = "trainingcenter"
    template_name = "training_center/delete.html"

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.organisation_slug = self.kwargs.get("organisation_slug", None)
        self.certifying_organisation = CertifyingOrganisation.objects.get(
            slug=self.organisation_slug
        )
        return super(TrainingCenterDeleteView, self).get(request, *args, **kwargs)

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

        self.organisation_slug = self.kwargs.get("organisation_slug", None)
        self.certifying_organisation = CertifyingOrganisation.objects.get(
            slug=self.organisation_slug
        )
        return super(TrainingCenterDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation list page
        for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse(
            "certifyingorganisation-detail",
            kwargs={
                "slug": self.object.certifying_organisation.slug,
            },
        )

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the CertifyingOrganisation objects by
        Project before passing to get_object() to ensure that we
        return the correct Certifying Organisation object.
        The requesting User must be authenticated.

        :returns: Certifying Organisation queryset filtered by Project.
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated:
            raise Http404
        qs = TrainingCenter.objects.filter(
            certifying_organisation=self.certifying_organisation
        )
        return qs


class TrainingCenterUpdateView(
    LoginRequiredMixin,
    ActiveCertifyingOrganisationRequiredMixin,
    TrainingCenterMixin,
    UpdateView,
):
    """Create view for Training Center."""

    context_object_name = "trainingcenter"
    template_name = "training_center/update.html"

    def get_success_url(self):
        """Define the redirect URL.

         After successful creation of the object, the User will be redirected
         to the Certifying Organisation detail page.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse(
            "certifyingorganisation-detail",
            kwargs={
                "slug": self.object.certifying_organisation.slug,
            },
        )

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(TrainingCenterUpdateView, self).get_context_data(**kwargs)
        context["trainingcenters"] = self.get_queryset().filter(
            certifying_organisation=self.certifying_organisation
        )
        context["organisation"] = self.certifying_organisation
        return context

    def form_valid(self, form):
        """Save new created Training Center.

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""

        try:
            super(TrainingCenterUpdateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                "ERROR: Training Center by this name already exists!"
            )

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(TrainingCenterUpdateView, self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get("organisation_slug", None)
        self.certifying_organisation = CertifyingOrganisation.objects.get(
            slug=self.organisation_slug
        )
        kwargs.update(
            {
                "user": self.request.user,
                "certifying_organisation": self.certifying_organisation,
            }
        )
        return kwargs
