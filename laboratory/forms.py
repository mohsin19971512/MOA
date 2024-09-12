from django import forms
from .models import HealthTest, PurityTest, MoistureTest, PlantTest,Lab,FungalExamination,PlantTest, SeedEntry
from lov.models import SampleComponents, SampleWeight,PurityTestCropType,PurityTestJungle
from django.forms import inlineformset_factory

from django.forms import formset_factory,modelformset_factory




#-------------------------------------------------------------------------------------------------------------------------------------

class MoistureTestForm(forms.ModelForm):
    sample_a_empty_box_weight = forms.FloatField(label="وزن العلبة الفارغة لعينة أ")
    sample_a_sample_weight_before_drying = forms.FloatField(label="وزن العينة قبل التجفيف لعينة أ")
    sample_a_sample_weight_after_drying = forms.FloatField(label="وزن العينة بعد التجفيف لعينة أ")
    result_a = forms.FloatField(label="ناتج عينة أ")

    sample_b_empty_box_weight = forms.FloatField(label="وزن العلبة الفارغة لعينة ب")
    sample_b_sample_weight_before_drying = forms.FloatField(label="وزن العينة قبل التجفيف لعينة ب")
    sample_b_sample_weight_after_drying = forms.FloatField(label="وزن العينة بعد التجفيف لعينة ب")
    result_b = forms.FloatField(label="ناتج عينة ب")

    class Meta:
        model = MoistureTest
        fields = [
            'Category', 'examination_method', 'oven_temperature', 'result_a','result_b',
            'number_of_drying_hours', 'initial_weight', 'humidity'
        ]
        widgets = {
            'Category': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'examination_method': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'oven_temperature': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'number_of_drying_hours': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'initial_weight': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'result_a': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'result_b': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),

            'humidity': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }



#-------------------------------------------------------------------------------------------------------------------------------------




class AssignmentForm(forms.Form):
    labs = forms.ModelMultipleChoiceField(
        queryset=Lab.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

class FungalExaminationForm(forms.ModelForm):
    class Meta:
        model = FungalExamination
        fields = [
            'common_scabies',
            'silver_scabies',
            'fusarium',
            'rhizoctonia',
        ]
        widgets = {
            'common_scabies': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
            'silver_scabies': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
            'fusarium': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
            'rhizoctonia': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
        }

class HealthTestForm(forms.ModelForm):
    class Meta:
        model = HealthTest
        fields = [
            'pest_infestation_percentage',
            'bacterial_infestation_percentage',
            'viral_infestation_percentage',
            'damage_percentage',
        ]
        widgets = {
            'pest_infestation_percentage': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
            'bacterial_infestation_percentage': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
            'viral_infestation_percentage': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
            'damage_percentage': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full'}),
        }



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
        fields = ['Incoming_sample_weight', 'purity_percentage', 'inert_materials_percentage', 'other_seeds_percentage']
        widgets = {
            'Incoming_sample_weight': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            # 'purity_percentage': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'inert_materials_percentage': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'other_seeds_percentage': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }
    
    purity_percentage = forms.FloatField(label='نسبة النقاء', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))

    # Additional fields for weight components
    weight_a = forms.FloatField(label='وزن A', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    weight_b = forms.FloatField(label='وزن B', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    pure_seeds_weight_a = forms.FloatField(label='وزن A للبذور النقية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    pure_seeds_weight_b = forms.FloatField(label='وزن B للبذور النقية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    inert_materials_weight_a = forms.FloatField(label='وزن A للمواد غير الحية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    inert_materials_weight_b = forms.FloatField(label='وزن B للمواد غير الحية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    other_seeds_weight_a = forms.FloatField(label='وزن A للبذور الأخرى', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
    other_seeds_weight_b = forms.FloatField(label='وزن B للبذور الأخرى', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))

    # Inline formsets for CropType and Jungle
    CropTypeFormSet = formset_factory(PurityTestCropTypeForm, extra=0)
    JungleFormSet = formset_factory(PurityTestJungleForm, extra=0)

    crop_type_forms = CropTypeFormSet()
    jungle_forms = JungleFormSet()








class PlantTestForm(forms.ModelForm):
    class Meta:
        model = PlantTest
        fields = [
            'number_of_seeds',
            'temperature',
            'planting_method',
            'tetrazonium_test',
            'seed_vitality',
            'germination_power',
            'duplicates'
        ]
        widgets = {
            'number_of_seeds': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'temperature': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'planting_method': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2 text-center'}),
            'tetrazonium_test': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'seed_vitality': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2 '}),
            'germination_power': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'duplicates': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2 text-center'})
        }


class SeedEntryForm(forms.ModelForm):
    class Meta:
        model = SeedEntry
        fields = [
            'seed_type', 'value_1', 'value_2', 'value_3', 'value_4',
            'value_5', 'value_6', 'value_7', 'value_8','count_date'
        ]
        labels = {
            'seed_type': 'نوع البذور',
            'value_1': 'القيمة  1',
            'value_2': 'القيمة 2',
            'value_3': 'القيمة 3',
            'value_4': 'القيمة 4',
            'value_5': 'القيمة 5',
            'value_6': 'القيمة 6',
            'value_7': 'القيمة 7',
            'value_8': 'القيمة 8',
            'count_date': 'تاريخ العد',
        }
        widgets = {
            'count_date': forms.DateInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2', 'type': 'date'}),
            'seed_type': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2 text-center'}),
            'value_1': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'value_2': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'value_3': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'value_4': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'value_5': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'value_6': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'value_7': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'value_8': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'})
        }

    def __init__(self, *args, **kwargs):
        duplicates = kwargs.pop('duplicates', '4x100')
        super().__init__(*args, **kwargs)
        
        # Customize widgets based on duplicates value
        if duplicates in ['4x100', '8x50']:
            for i in range(5, 9):
                self.fields[f'value_{i}'].widget = forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'})
        else:
            # Handle unexpected duplicates values if needed
            raise ValueError("Unexpected value for duplicates")


# class PurityTestForm(forms.ModelForm):
#     class Meta:
#         model = PurityTest
#         fields = ['Incoming_sample_weight', 'purity_percentage', 'inert_materials_percentage', 'other_seeds_percentage']
#         widgets = {
#             'Incoming_sample_weight': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
#             'purity_percentage': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
#             'inert_materials_percentage': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
#             'other_seeds_percentage': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
#         }

#     # Additional fields for weight components
#     weight_a = forms.FloatField(label='وزن A', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
#     weight_b = forms.FloatField(label='وزن B', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
#     pure_seeds_weight_a = forms.FloatField(label='وزن A للبذور النقية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
#     pure_seeds_weight_b = forms.FloatField(label='وزن B للبذور النقية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
#     inert_materials_weight_a = forms.FloatField(label='وزن A للمواد غير الحية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
#     inert_materials_weight_b = forms.FloatField(label='وزن B للمواد غير الحية', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
#     other_seeds_weight_a = forms.FloatField(label='وزن A للبذور الأخرى', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))
#     other_seeds_weight_b = forms.FloatField(label='وزن B للبذور الأخرى', widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}))