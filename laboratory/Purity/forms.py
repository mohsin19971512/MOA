from django import forms
from django.forms import formset_factory

from laboratory.Purity.models import PurityTest
from lov.models import PurityTestCropType, PurityTestJungle


class PurityTestCropTypeForm(forms.ModelForm):
    class Meta:
        model = PurityTestCropType
        fields = ['crop_type', 'count']
        widgets = {
            'count': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }

class PurityTestJungleForm(forms.ModelForm):
    class Meta:
        model = PurityTestJungle
        fields = ['jungle', 'count']
        widgets = {
            'count': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }


class CropTypeCountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        crop_types = kwargs.pop('crop_types', None)
        super().__init__(*args, **kwargs)
        if crop_types:
            for crop_type in crop_types:
                self.fields[f'crop_type_{crop_type.id}'] = forms.IntegerField(
                    label=crop_type.name,
                    widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
                    required=False
                )






class JungleCountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        jungles = kwargs.pop('jungles', None)
        super().__init__(*args, **kwargs)
        if jungles:
            for jungle in jungles:
                self.fields[f'jungle_{jungle.id}'] = forms.IntegerField(
                    label=jungle.name,
                    widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-500 rounded-md p-2'}),
                    required=False
                )










class PurityTestForm(forms.ModelForm):
    class Meta:
        model = PurityTest
        fields = ['Incoming_sample_weight', 'unit_of_measure', 'purity_percentage', 'inert_materials_percentage',
                  'other_seeds_percentage']
        widgets = {
            'Incoming_sample_weight': forms.NumberInput(
                attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'unit_of_measure': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'inert_materials_percentage': forms.NumberInput(
                attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'other_seeds_percentage': forms.NumberInput(
                attrs={'class': 'w-full border  border-gray-300 rounded-md p-2'}),
        }

    purity_percentage = forms.FloatField(label='نسبة النقاء', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))

    # Additional fields for weight components
    weight_a = forms.FloatField(label='وزن A', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    weight_b = forms.FloatField(label='وزن B', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    pure_seeds_weight_a = forms.FloatField(label='وزن A للبذور النقية', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    pure_seeds_weight_b = forms.FloatField(label='وزن B للبذور النقية', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    inert_materials_weight_a = forms.FloatField(label='وزن A للمواد غير الحية', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    inert_materials_weight_b = forms.FloatField(label='وزن B للمواد غير الحية', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    other_seeds_weight_a = forms.FloatField(label='وزن A للبذور الأخرى', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    other_seeds_weight_b = forms.FloatField(label='وزن B للبذور الأخرى', widget=forms.NumberInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))

    # Inline formsets for CropType and Jungle
    CropTypeFormSet = formset_factory(PurityTestCropTypeForm, extra=0)
    JungleFormSet = formset_factory(PurityTestJungleForm, extra=0)

    crop_type_forms = CropTypeFormSet()
    jungle_forms = JungleFormSet()