from django import forms
from django.forms import ModelForm
from .models import Atten,Attenwork
from datetime import datetime,date




class DateInput(forms.DateInput):
    input_type='date'

class AttendForm(forms.ModelForm):
    class Meta:
        model = Atten
        fields = [ 'Name', 'Dept','Joining','Date']
        
class AttenworkForm(ModelForm):
    class Meta:
        model=Attenwork
        fields ='__all__'
        
        