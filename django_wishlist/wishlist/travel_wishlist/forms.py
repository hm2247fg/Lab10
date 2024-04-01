from django import forms
from .models import Place


class NewPlaceForm(forms.ModelForm):
    # Form class for adding a new place
    # Specifies the model and fields to be used in the form
    class Meta:
        model = Place
        fields = ('name', 'visited')
