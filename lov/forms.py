from django import forms
from .models import SampleWeight, SampleComponents
from laboratory.models import PurityTest
class SampleWeightForm(forms.ModelForm):
    class Meta:
        model = SampleWeight
        fields = ['weight_a', 'weight_b']

class SampleComponentsForm(forms.ModelForm):
    class Meta:
        model = SampleComponents
        fields = ['component_type', 'weight']

class PurityTestForm(forms.ModelForm):
    class Meta:
        model = PurityTest
        fields = ['Incoming_sample_weight', 'purity_percentage', 'inert_materials_percentage', 'other_seeds_percentage']
    
    # Adding the SampleWeightForm and SampleComponentsForm fields
    weight_a = forms.FloatField(label='Weight A')
    weight_b = forms.FloatField(label='Weight B')
    pure_seeds_weight_a = forms.FloatField(label='Pure Seeds Weight A')
    pure_seeds_weight_b = forms.FloatField(label='Pure Seeds Weight B')
    inert_materials_weight_a = forms.FloatField(label='Inert Materials Weight A')
    inert_materials_weight_b = forms.FloatField(label='Inert Materials Weight B')
    other_seeds_weight_a = forms.FloatField(label='Other Seeds Weight A')
    other_seeds_weight_b = forms.FloatField(label='Other Seeds Weight B')
