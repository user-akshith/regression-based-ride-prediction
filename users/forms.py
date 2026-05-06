from django import forms

class PredictionForm(forms.Form):
    distance_km = forms.FloatField()
    time_of_day = forms.ChoiceField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('Night', 'Night')])
    hour_of_day = forms.IntegerField(min_value=0, max_value=23)
    day_of_week = forms.ChoiceField(choices=[('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),
                                              ('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday'),('Sunday','Sunday')])
    weather = forms.ChoiceField(choices=[('Clear', 'Clear'), ('Rainy', 'Rainy'), ('Cloudy', 'Cloudy'), ('Snowy', 'Snowy')])
    uv_index = forms.FloatField(min_value=0, max_value=11)
    moon_phase = forms.ChoiceField(choices=[('New Moon', 'New Moon'), ('Full Moon', 'Full Moon'),
                                            ('First Quarter', 'First Quarter'), ('Last Quarter', 'Last Quarter')])

from django import forms
from .models import UserRegistrationModel


class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-zA-Z]+'}), required=True, max_length=100)
    loginid = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-zA-Z]+'}), required=True, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
                                                                 'title': 'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters'}),
                               required=True, max_length=100)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[56789][0-9]{9}'}), required=True,
                             max_length=100)
    email = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'}),
                            required=True, max_length=100)
    locality = forms.CharField(widget=forms.TextInput(), required=True, max_length=100)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 22}), required=True, max_length=250)
    city = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}), required=True,
        max_length=100)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}), required=True,
        max_length=100)
    status = forms.CharField(widget=forms.HiddenInput(), initial='waiting', max_length=100)

    class Meta():
        model = UserRegistrationModel
        fields = '__all__'