from django import forms
from .models import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ["name", "latitude", "longitude"]


class LocationForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    distance = forms.FloatField()
