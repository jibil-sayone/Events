from django import forms
from django.forms import ModelForm

from .models import *
class EventForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder':' Add new Event...'}))
    class Meta:
        model=Event
        fields= ['title','description','location','start_date','end_date','categories']