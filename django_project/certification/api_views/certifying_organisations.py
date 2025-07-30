from base.models.project import Project
from certification.models import CertifyingOrganisation
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.organisation_serializer import CertifyingOrganisationSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = (
        "page_size"  # Allow client to override the page size via query parameter
    )
    max_page_size = 100  # Maximum limit allowed

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page_size": self.get_page_size(self.request),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class CertifyingOrganisationApiListView(APIView):
    """
    API view to list all certifying organisations with pagination and optional filtering.

    Available query parameters:
    - country: Filter organisations by one or more country codes (comma-separated, e.g., ZA or ZA,MG,NL) (optional)
    - page: Page number to retrieve (default: 1)
    - page_size: Number of items per page (default: 10, max: 100)
    """

    # Apply pagination class
    pagination_class = CustomPagination

    def get(self, request):
        """
        Handle GET requests to list certifying organisations.

        Returns paginated response with:
        - count: Total number of items
        - page_size: Number of items per page
        - next: URL to next page (if exists)
        - previous: URL to previous page (if exists)
        - results: List of organisations for current page
        """
        country_param = request.query_params.get("country")
        project = Project.objects.get(slug="qgis")
        organisations = CertifyingOrganisation.approved_objects.filter(
            project=project, is_archived=False
        )

        if country_param:
            country_codes = [
                c.strip().upper() for c in country_param.split(",") if c.strip()
            ]
            organisations = organisations.filter(country__in=country_codes)

        # Paginate the queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(organisations, request)

        if page is not None:
            serializer = CertifyingOrganisationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Fallback for non-paginated response if needed
        serializer = CertifyingOrganisationSerializer(organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
