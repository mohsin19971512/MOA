from django import forms

from laboratory.Plan.models import PlantTest, SeedEntry


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
            'duplicates',
            'agriculture_date'
        ]
        widgets = {
            'number_of_seeds': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'temperature': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'planting_method': forms.Select
                (attrs={'class': 'w-full border border-gray-600 rounded-md p-2 text-center'}),
            'tetrazonium_test': forms.TextInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'seed_vitality': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2 '}),
            'germination_power': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'duplicates': forms.Select(attrs={'class': 'w-full border border-gray-600 rounded-md p-2 text-center'}),
            'agriculture_date': forms.DateInput
            (attrs={'class': 'w-full border border-gray-600 rounded-md p-2', 'type': 'date'}),
        }


class SeedEntryForm(forms.ModelForm):
    class Meta:
        model = SeedEntry
        fields = [
            'seed_type', 'value_1', 'value_2', 'value_3', 'value_4',
            'value_5', 'value_6', 'value_7', 'value_8' ,'count_date'
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
            'count_date': forms.DateInput
                (attrs={'class': 'w-full border border-gray-600 rounded-md p-2', 'type': 'date'}),
            'seed_type': forms.Select(attrs={'class': 'w-full border border-gray-600 rounded-md p-2 text-center'}),
            'value_1': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'value_2': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'value_3': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'value_4': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'value_5': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'value_6': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'value_7': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'}),
            'value_8': forms.NumberInput(attrs={'class': 'w-full border border-gray-600 rounded-md p-2'})
        }

    def __init__(self, *args, **kwargs):
        duplicates = kwargs.pop('duplicates', '4x100')
        super().__init__(*args, **kwargs)

        # Customize widgets based on duplicates value
        if duplicates in ['4x100', '8x50']:
            for i in range(5, 9):
                self.fields[f'value_{i}'].widget = forms.NumberInput \
                    (attrs={'class': 'w-full border border-gray-300 rounded-md p-2'})
        else:
            # Handle unexpected duplicates values if needed
            raise ValueError("Unexpected value for duplicates")
