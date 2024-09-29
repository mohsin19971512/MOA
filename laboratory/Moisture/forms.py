#-------------------------------------------------------------------------------------------------------------------------------------
from django import forms

from laboratory.Moisture.models import MoistureTest


class MoistureTestForm(forms.ModelForm):
    sample_a_empty_box_weight = forms.FloatField(label="وزن العلبة الفارغة لعينة أ", required=False)
    sample_a_sample_weight_before_drying = forms.FloatField(label="وزن العينة قبل التجفيف لعينة أ", required=False)
    sample_a_sample_weight_after_drying = forms.FloatField(label="وزن العينة بعد التجفيف لعينة أ", required=False)
    result_a = forms.FloatField(label="ناتج عينة أ", required=False)

    sample_b_empty_box_weight = forms.FloatField(label="وزن العلبة الفارغة لعينة ب", required=False)
    sample_b_sample_weight_before_drying = forms.FloatField(label="وزن العينة قبل التجفيف لعينة ب", required=False)
    sample_b_sample_weight_after_drying = forms.FloatField(label="وزن العينة بعد التجفيف لعينة ب", required=False)
    result_b = forms.FloatField(label="ناتج عينة ب", required=False)

    class Meta:
        model = MoistureTest
        fields = [
            'Category', 'examination_method', 'oven_temperature', 'result_a', 'result_b',
            'number_of_drying_hours', 'initial_weight', 'unit_of_measure', 'humidity'
        ]
        widgets = {
            'Category': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'examination_method': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'oven_temperature': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'number_of_drying_hours': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'initial_weight': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'unit_of_measure': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'result_a': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'result_b': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'humidity': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }