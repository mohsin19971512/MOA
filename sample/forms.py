from django import forms

from laboratory.Health.models import HealthTest
from .models import Sample

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = [
            'crop_name', 'distinguishing_marks', 'sample_id', 'shipment_weight', 'unit_of_measure',
            'location', 'sender_name', 'sample_type', 'the_draw', 'batch_number', 'received_date',
            'the_divider', 'test_type',
            'treatment_type'
        ]
        widgets = {
            'received_date': forms.DateInput(attrs={'type': 'date'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'result_date': forms.DateInput(attrs={'type': 'date'}),
        }

class HealthTestNotesForm(forms.ModelForm):
    class Meta:
        model = HealthTest
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }