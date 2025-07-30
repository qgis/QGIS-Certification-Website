from certification.models import CertifyingOrganisation
from rest_framework import serializers


class CertifyingOrganisationSerializer(serializers.ModelSerializer):
    """Serializer for Certifying Organisation model."""

    country_name = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()

    class Meta:
        model = CertifyingOrganisation
        fields = [
            "name",
            "country_name",
            "country_code",
            "organisation_email",
            "url",
            "address",
            "organisation_phone",
        ]

    def get_country_name(self, obj):
        """Get the name of the country."""
        return obj.country.name if obj.country else None

    def get_country_code(self, obj):
        """Get the ISO 3166-1 alpha-2 code of the country."""
        return obj.country.code if obj.country else None
