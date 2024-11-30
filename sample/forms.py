from django import forms
from laboratory.Health.models import HealthTest
from .models import Sample


class SampleForm(forms.ModelForm):


    class Meta:
        model = Sample
        fields = [
            'crop_name', 'distinguishing_marks', 'sample_id', 'shipment_weight', 'unit_of_measure',
            'location', 'sender_name', 'sample_type', 'the_draw','withdrawal_date', 'batch_number', 'received_date',
            'the_divider', 'test_type', 'treatment_type', 'test_type'
        ]
        widgets = {
            'received_date': forms.DateInput(attrs={'type': 'date'}),
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'result_date': forms.DateInput(attrs={'type': 'date'}),
            'withdrawal_date' : forms.DateInput(attrs={'type': 'date'}),
            'test_type' : forms.Textarea(attrs={'type': 'text'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user from kwargs
        super(SampleForm, self).__init__(*args, **kwargs)

        if user and user.profile.user_role == 'Applicant':
            # Include only specific fields for role1
            self.fields = {key: self.fields[key] for key in [
                'sample_id','crop_name',  'treatment_type', 'the_divider','received_date',
                'sample_type','test_type'
            ]}
        elif user and user.profile.user_role == 'Altarmiz':
            # Exclude certain fields for role2
            exclude_fields = ['crop_name',  'treatment_type', 'the_divider','received_date','sample_type','test_type']
            for field in exclude_fields:
                self.fields.pop(field, None)

        # Conditionally make fields read-only
        readonly_fields = []
        if user and user.profile.user_role == 'Applicant':
            readonly_fields = ['sample_id',]
        # elif user and user.profile.user_role == 'Altarmiz':
        #     readonly_fields = ['received_date', 'location']

        for field in readonly_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['readonly'] = 'readonly'

class HealthTestNotesForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }

