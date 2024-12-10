from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Offer
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

class OfferForm(forms.ModelForm):
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
        model = Offer
        fields = [
            'title',
            'description',
            'location_type',
            'address',
            'latitude',
            'longitude',
            'category',
            'status',
            'quantity',
            'availability_start',
            'availability_end'
        ]
        help_texts = {
            'address': 'Enter your address.',
            'latitude': 'Enter your latitude coordinate.',
            'longitude': 'Enter your longitude coordinate.',
            'availability_start': 'Start date and time when the offer is available.',
            'availability_end': 'End date and time when the offer is no longer available.',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability_start': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
            'availability_end': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        # set the initial value of location_type based on the instance( long and lat or address)
        if self.instance and self.instance.location_type:
            self.fields['location_type'].initial = self.instance.location_type

    def clean_availability_start(self):
        availability_start = self.cleaned_data.get('availability_start')
        if availability_start and availability_start < timezone.now():
            raise ValidationError("The start date and time must be in the future.")
        return availability_start

    def clean_availability_end(self):
        availability_start = self.cleaned_data.get('availability_start')
        availability_end = self.cleaned_data.get('availability_end')
        if availability_end and availability_start:
            if availability_end < availability_start:
                raise ValidationError("The end date and time cannot be before the start date and time.")
        return availability_end

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
                # check if the address is valid
                geolocator = Nominatim(user_agent="CORE")
                try:
                    location = geolocator.geocode(address, timeout=10)
                    if location is None:
                        self.add_error('address', "Please provide a valid address.")
                    else:
                        # we can implement storing the geocoded latitude and longitude
                        # cleaned_data['latitude'] = location.latitude
                        # cleaned_data['longitude'] = location.longitude
                        pass
                except GeocoderServiceError:
                    # Handle geocoding service errors, as this is a free api it may have some limitations
                    self.add_error('address', "Geocoding service error. Please try again later.")
                except Exception as e:
                    self.add_error('address', "An error occurred while validating the address.")
            # clear latitude and longitude
            cleaned_data['latitude'] = None
            cleaned_data['longitude'] = None
        elif location_type == 'coordinates':
            if latitude is None or longitude is None:
                if latitude is None:
                    self.add_error('latitude', "Please provide latitude.")
                if longitude is None:
                    self.add_error('longitude', "Please provide longitude.")
            else:
                # validate latitude and longitude ranges
                if not (-90 <= latitude <= 90):
                    self.add_error('latitude', 'Latitude must be between -90 and 90.')
                if not (-180 <= longitude <= 180):
                    self.add_error('longitude', 'Longitude must be between -180 and 180.')
            # clear address
            cleaned_data['address'] = "No address provided"
        else:
            raise ValidationError("Invalid location type selected.")

        return cleaned_data
