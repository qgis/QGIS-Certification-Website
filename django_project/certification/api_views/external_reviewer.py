from braces.views import UserPassesTestMixin
from django.http.response import Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView

from base.models import Project


class UpdateExternalReviewerText(UserPassesTestMixin, APIView):
    """API to update external reviewer email text."""

    project = None

    def test_func(self, user):
        self.project = (
            Project.objects.get(
                slug='qgis')
        )

        return (
            user.is_staff or
            user == self.project.owner or
            user in self.project.certification_managers.all()
        )

    def post(self, request):
        email_text = request.POST.get('text', '')
        if not email_text:
            raise Http404('Missing required data')

        self.project.external_reviewer_invitation = (
            email_text
        )
        self.project.save()

        return HttpResponseRedirect(
            reverse('certification-management-view')
        )
