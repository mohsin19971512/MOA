from django import forms
from .models import Sample

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = [
            'sample_id', 'crop_name', 'shipment_weight', 'unit_of_measure', 'batch_number',
            'crop_type', 'variety', 'grade', 'sample_type', 'test_type', 'treatment_type',
            'sample_date', 'received_date', 'distinguishing_marks', 'sender_name'
        ]
        widgets = {
            'sample_date': forms.DateInput(attrs={'type': 'date'}),
            'received_date': forms.DateInput(attrs={'type': 'date'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'result_date': forms.DateInput(attrs={'type': 'date'}),
        }

