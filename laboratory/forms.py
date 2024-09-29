from django import forms
from .models import  Lab
from lov.models import SampleComponents, SampleWeight





class AssignmentForm(forms.Form):
    labs = forms.ModelMultipleChoiceField(
        queryset=Lab.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )



class SampleWeightForm(forms.ModelForm):
    class Meta:
        model = SampleWeight
        fields = ['weight_a', 'weight_b']
        widgets = {
            'weight_a': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'weight_b': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }


class SampleComponentsForm(forms.ModelForm):
    class Meta:
        model = SampleComponents
        fields = ['component_type', 'weight']
        widgets = {
            'component_type': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'weight': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }




