from django import forms
from django.forms import modelformset_factory

from laboratory.Health.models import HealthTest, InsectExamination, FungalExamination, BacterialExamination, \
    NematodeTest, ViralTest


# Health Form
class HealthTestForm(forms.ModelForm):
    class Meta:
        model = HealthTest
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'mt-1 p-2 border border-gray-600 rounded-md w-full'}),
        }


# Insect Examination Form
class InsectExaminationForm(forms.ModelForm):
    class Meta:
        model = InsectExamination
        fields = ['infection_type', 'cause', 'infection_percentage']
        widgets = {
            'infection_type': forms.Select(attrs={'class': 'mb-4 p-2 border border-gray-600 rounded-md text-center w-full'}),
            'cause': forms.Select(attrs={'class': 'mb-4  p-2 border border-gray-600 rounded-md w-full text-center'}),

            'infection_percentage': forms.NumberInput(attrs={'class': 'mt-1 p-2 border border-gray-600 rounded-md w-full'}),
        }


# Fungal Examination Form
class FungalExaminationForm(forms.ModelForm):
    class Meta:
        model = FungalExamination
        fields = ['cause','infection_percentage']
        widgets = {
            'cause': forms.Select(attrs={'class': 'mb-4 p-2 border border-gray-600 rounded-md w-full text-center'}),
            'infection_percentage': forms.NumberInput(attrs={'class': 'mb-4 mb-2 p-2 border border-gray-600 rounded-md w-full text-center'}),
        }


# Bacterial Examination Form
class BacterialExaminationForm(forms.ModelForm):
    class Meta:
        model = BacterialExamination
        fields = ['cause','infection_type','damage_percentage', 'greenness_percentage']
        widgets = {
            'cause': forms.Select(attrs={'class': 'mb-1 p-2 border border-gray-600 rounded-md w-full text-center'}),
            'infection_type': forms.Select(attrs={'class': 'mb-1 p-2 border border-gray-600 rounded-md text-center w-full'}),
            'damage_percentage': forms.NumberInput(attrs={'class': 'mb-1 p-2 border border-gray-600 rounded-md w-full'}),
            'greenness_percentage': forms.NumberInput(attrs={'class': 'mb-1 p-2 border border-gray-600 rounded-md w-full'}),
        }


# Seed Health Test Form


# Nematode Test Form
class NematodeTestForm(forms.ModelForm):
    class Meta:
        model = NematodeTest
        fields = ['warts_count']
        widgets = {
            'warts_count': forms.NumberInput(attrs={'class': 'mt-4 p-2 border border-gray-600 rounded-md w-full'}),
        }


# Viral Test Form
class ViralTestForm(forms.ModelForm):
    class Meta:
        model = ViralTest
        fields = ['infection_type', 'cause','infection_rate']
        widgets = {
            'infection_type': forms.Select(attrs={'class': 'mt-4 p-2 border border-gray-600 rounded-md w-full text-center'}),
            'cause': forms.Select(attrs={'class': 'mt-4  p-2 border border-gray-600 rounded-md w-full text-center'}),

            'infection_rate': forms.NumberInput(attrs={'class': 'mt-2 p-2 border border-gray-600 rounded-md w-full'}),
        }


# Create formsets for the model forms
InsectExaminationFormSet = modelformset_factory(InsectExamination, form=InsectExaminationForm, extra=3)
FungalExaminationFormSet = modelformset_factory(FungalExamination, form=FungalExaminationForm, extra=2)