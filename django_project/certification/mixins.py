from certification.models import CertifyingOrganisation
from django.http import Http404


class ActiveCertifyingOrganisationRequiredMixin:
    """Mixin to ensure that the certifyin organisation is not archived."""

    def dispatch(self, request, *args, **kwargs):
        organisation_slug = kwargs.get("organisation_slug") or kwargs.get("slug")
        try:
            organisation = CertifyingOrganisation.objects.get(slug=organisation_slug)
        except CertifyingOrganisation.DoesNotExist:
            raise Http404("Organisation does not exist.")
        if organisation.is_archived:
            raise Http404("This organisation is archived.")
        return super().dispatch(request, *args, **kwargs)
