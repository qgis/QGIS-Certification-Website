# coding=utf-8
"""Tools for Certification app."""
from django.contrib.gis.serializers.geojson import Serializer
import requests
import hmac
import hashlib
from django.conf import settings
import base64
import urllib
from urllib.parse import urlencode, quote, quote_plus

def check_slug(queryset, slug):
    """
    This function checks slug within a model queryset
    and return a new incremented slug when there are duplicates.

    """

    registered_slug = queryset.values_list('slug', flat=True)
    new_slug = slug
    if slug in registered_slug:
        match_slug = [s for s in registered_slug if slug in s]
        num = len(match_slug)
        new_slug = str(num) + '-' + slug

    return new_slug


class CustomSerializer(Serializer):
    """Custom serializer to return the name of the foreign key object."""

    def end_object(self, obj):
        for field in self.selected_fields:
            if field == 'pk':
                continue
            elif field in self._current.keys():
                continue
            else:
                try:
                    if '__' in field:
                        fields = field.split('__')
                        value = obj
                        for f in fields:
                            value = getattr(value, f)
                        if value != obj:
                            self._current[field] = value

                except AttributeError:
                    pass
        super(CustomSerializer, self).end_object(obj)


class PayrexxService:
    def __init__(self):
        self.instance_name = settings.PAYREXX_INSTANCE
        self.api_secret = settings.PAYREXX_API_SECRET
        self.base_url = f"https://api.payrexx.com/v1.0/"
    
    def generate_signature(self, query_string):
        signature = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return base64.b64encode(signature.digest()).decode('utf-8')

    def flatten_dict(self, dictionary, parent_key=''):
        flattened_data = {}
        for key, value in dictionary.items():
            new_key = f"{parent_key}[{key}]" if parent_key else key
            if isinstance(value, dict):
                flattened_data.update(self.flatten_dict(value, new_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened_data.update(self.flatten_dict(item, f"{new_key}[{i}]"))
                    else:
                        flattened_data[f"{new_key}[{i}]"] = item
            else:
                flattened_data[new_key] = value
        return flattened_data

    def encode_query_string(self, data):
        encoded_pairs = []
        for key, value in data.items():
            encoded_key = quote(key, safe='')
            if isinstance(value, list):
                for item in value:
                    encoded_pairs.append(f"{encoded_key}={quote(str(item), safe='')}")
            else:
                encoded_pairs.append(f"{encoded_key}={quote(str(value), safe='')}")
        return '&'.join(encoded_pairs)
    
    def prepare_data(self, raw_data):
        # Flatten the rawData
        data = self.flatten_dict(raw_data)

        # Create Query String
        query_string = urlencode(data, quote_via=quote_plus)

        # Generate the API Signature
        api_signature = self.generate_signature(query_string)

        # Add the API signature to the data payload
        data['ApiSignature'] = api_signature

        # Generate QueryString for the Request
        return self.encode_query_string(data)

    def create_gateway(
            self,
            amount,
            currency,
            purpose,
            redirect_url,
            firstname: str = '',
            lastname: str = '',
            email: str = '',
            **kwargs
        ):
        """Create a payment gateway"""
        endpoint = "Gateway/"
        url = f"{self.base_url}{endpoint}?instance={self.instance_name}"
        
        amount = amount * 100  # Convert to cents
        raw_data = {
            'amount': str(amount),
            'currency': currency,
            'purpose': purpose,
            'successRedirectUrl': redirect_url,
            'fields': {
                'forename': {'value': firstname},
                'surname': {'value': lastname},
                'email': {'value': email}
            },
        }

        # Generate QueryString for the Request
        request_query_string = self.prepare_data(raw_data)

        # Make the POST request
        response = requests.post(f"{url}", data=request_query_string)
        return response.json()

    def get_gateway(self, gateway_id):
        """Retrieve gateway information"""
        endpoint = f"Gateway/{gateway_id}/"
        url = f"{self.base_url}{endpoint}?instance={self.instance_name}"
        raw_data = {}
        # Generate QueryString for the Request
        request_query_string = self.prepare_data(raw_data)
        # Make the GET request
        response = requests.get(f"{url}{endpoint}", data=request_query_string)
        return response.json()
