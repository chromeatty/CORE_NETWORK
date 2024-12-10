from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Profile

class SignUpForm(UserCreationForm):
    # Adding a user_type field with choices defined in the User model
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, 
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'user_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        #  custom attributes to name, email and username fields
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Full Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        

        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})



from django.core.exceptions import ValidationError
# use geopy and the nominatim geocoder for address validation and longitude/latitude retrieval
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

class ProfileForm(forms.ModelForm):
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
        model = Profile
        fields = [
            'contact_info',
            'service_areas',
            'preferences',
            'privacy_settings',
            'location_type',
            'address',
            'latitude',
            'longitude',
        ]
        help_texts = {
            'address': 'Enter your address.',
            'latitude': 'Enter your latitude coordinate.',
            'longitude': 'Enter your longitude coordinate.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initial value of location_type based on the instance
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
                # Geocode the address to check if it's valid
                geolocator = Nominatim(user_agent="your_app_name")  # Replace with your app's name
                try:
                    location = geolocator.geocode(address, timeout=10)
                    if location is None:
                        self.add_error('address', "Please provide a valid address.")
                    else:
                        # store the geocoded latitude and longitude, not using
                        # cleaned_data['latitude'] = location.latitude
                        # cleaned_data['longitude'] = location.longitude
                        pass
                except GeocoderServiceError:
                    self.add_error('address', "Geocoding service error. Please try again later.")
                except Exception as e:
                    self.add_error('address', "An error occurred while validating the address.")
            # clear the latitude and longitude
            cleaned_data['latitude'] = None
            cleaned_data['longitude'] = None
        elif location_type == 'coordinates':
            if latitude is None or longitude is None:
                if latitude is None:
                    self.add_error('latitude', "Please provide latitude.")
                if longitude is None:
                    self.add_error('longitude', "Please provide longitude.")
            else:
                # ensure that latitude and longitude are within valid ranges
                if not (-90 <= latitude <= 90):
                    self.add_error('latitude', 'Latitude must be between -90 and 90.')
                if not (-180 <= longitude <= 180):
                    self.add_error('longitude', 'Longitude must be between -180 and 180.')
            # Clear address
            cleaned_data['address'] = "No address provided"
        else:
            raise ValidationError("Invalid location type selected.")

        # Update the instance's location_type
        self.instance.location_type = location_type

        return cleaned_data


    
class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember Me')
    # put a placeholder for the username and password feilds
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct username and password. Note that both fields may be case-sensitive."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )
        
"""
class UserLoginOut(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember Me')
    # put a placeholder for the username and password feilds
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct username and password. Note that both fields may be case-sensitive."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )
"""