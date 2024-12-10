from django import forms
from django.core.exceptions import ValidationError
from .models import Request
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

class RequestForm(forms.ModelForm):
    LOCATION_CHOICES = [
        ('address', 'Address'),
        ('coordinates', 'Latitude and Longitude'),
    ]

    location_type = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Location Type',
        help_text='Select how you would like to provide your location.'
    )

    class Meta:
        model = Request
        fields = [
            'title',
            'description',
            'location_type',
            'address',
            'latitude',
            'longitude',
            'category',
            'urgency',
            'status'
        ]
        help_texts = {
            'address': 'Enter your address.',
            'latitude': 'Enter your latitude coordinate.',
            'longitude': 'Enter your longitude coordinate.',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)

        # made the location_type field required to prevent errors of not selecting a location type
        if self.instance and self.instance.location_type:
            self.fields['location_type'].initial = self.instance.location_type

    def clean(self):
        cleaned_data = super().clean()
        location_type = cleaned_data.get('location_type')
        address = cleaned_data.get('address')
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        if location_type == 'address':
            if not address or address.strip() == '' or address == "No address provided":
                self.add_error('address', "Please provide an address.")
            else:
                # check the Geocoding service to see if the address is valid
                geolocator = Nominatim(user_agent="your_app_name")  # Replace with your app's name
                try:
                    location = geolocator.geocode(address, timeout=10)
                    if location is None:
                        self.add_error('address', "Please provide a valid address.")
                    else:
                        # not using the location data
                        # cleaned_data['latitude'] = location.latitude
                        # cleaned_data['longitude'] = location.longitude
                        pass
                except GeocoderServiceError:
                    self.add_error('address', "Geocoding service error. Please try again later.")
                except Exception as e:
                    self.add_error('address', "An error occurred while validating the address.")
            # latitude and longitude cleared
            cleaned_data['latitude'] = None
            cleaned_data['longitude'] = None
        elif location_type == 'coordinates':
            if latitude is None or longitude is None:
                if latitude is None:
                    self.add_error('latitude', "Please provide latitude.")
                if longitude is None:
                    self.add_error('longitude', "Please provide longitude.")
            else:
                # ensure that the latitude and longitude are within the valid range
                if not (-90 <= latitude <= 90):
                    self.add_error('latitude', 'Latitude must be between -90 and 90.')
                if not (-180 <= longitude <= 180):
                    self.add_error('longitude', 'Longitude must be between -180 and 180.')
            cleaned_data['address'] = "No address provided"
        else:
            raise ValidationError("Invalid location type selected.")

        return cleaned_data
