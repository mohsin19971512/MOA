# -------------------------------------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from laboratory.Moisture.forms import MoistureTestForm
from laboratory.Moisture.models import MoistureSample, MoistureTest
from laboratory.models import Assignment
from django.urls import reverse


@login_required
def create_moisture_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample

    if request.method == 'POST':
        form = MoistureTestForm(request.POST)

        if form.is_valid():
            sample_a = None
            sample_b = None

            # Create the MoistureSample instances for sample_a if values are provided
            if form.cleaned_data['sample_a_empty_box_weight'] is not None:
                sample_a = MoistureSample.objects.create(
                    component_type='sample_a',
                    empty_box_weight=form.cleaned_data['sample_a_empty_box_weight'],
                    sample_weight_before_drying=form.cleaned_data['sample_a_sample_weight_before_drying'],
                    sample_weight_after_drying=form.cleaned_data['sample_a_sample_weight_after_drying'],
                    result=form.cleaned_data['result_a']
                )

            # Create the MoistureSample instances for sample_b if values are provided
            if form.cleaned_data['sample_b_empty_box_weight'] is not None:
                sample_b = MoistureSample.objects.create(
                    component_type='sample_b',
                    empty_box_weight=form.cleaned_data['sample_b_empty_box_weight'],
                    sample_weight_before_drying=form.cleaned_data['sample_b_sample_weight_before_drying'],
                    sample_weight_after_drying=form.cleaned_data['sample_b_sample_weight_after_drying'],
                    result=form.cleaned_data['result_b']
                )

            # Create the MoistureTest instance
            moisture_test = form.save(commit=False)
            moisture_test.assignment = assignment

            if sample_a:
                moisture_test.sample_a = sample_a

            if sample_b:
                moisture_test.sample_b = sample_b

            moisture_test.save()

            # Mark the assignment as completed
            assignment.completed = True
            assignment.save()

            return redirect(
                reverse('laboratory:moisture_test_detail', args=[assignment_id]))  # Redirect to success page
    else:
        form = MoistureTestForm()

    return render(request, 'laboratory/create_moisture_test.html', {
        'form': form,
        'sample': sample,
    })


@login_required
def update_moisture_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    moisture_test = get_object_or_404(MoistureTest, assignment=assignment)
    sample_a = moisture_test.sample_a
    sample_b = moisture_test.sample_b

    if request.method == 'POST':
        form = MoistureTestForm(request.POST, instance=moisture_test)

        if form.is_valid():
            # Check if sample_a exists before updating
            if sample_a:
                sample_a.empty_box_weight = form.cleaned_data.get('sample_a_empty_box_weight',
                                                                  sample_a.empty_box_weight)
                sample_a.sample_weight_before_drying = form.cleaned_data.get('sample_a_sample_weight_before_drying',
                                                                             sample_a.sample_weight_before_drying)
                sample_a.sample_weight_after_drying = form.cleaned_data.get('sample_a_sample_weight_after_drying',
                                                                            sample_a.sample_weight_after_drying)
                sample_a.result = form.cleaned_data.get('result_a', sample_a.result)
                sample_a.save()

            # Check if sample_b exists before updating
            if sample_b:
                sample_b.empty_box_weight = form.cleaned_data.get('sample_b_empty_box_weight',
                                                                  sample_b.empty_box_weight)
                sample_b.sample_weight_before_drying = form.cleaned_data.get('sample_b_sample_weight_before_drying',
                                                                             sample_b.sample_weight_before_drying)
                sample_b.sample_weight_after_drying = form.cleaned_data.get('sample_b_sample_weight_after_drying',
                                                                            sample_b.sample_weight_after_drying)
                sample_b.result = form.cleaned_data.get('result_b', sample_b.result)
                sample_b.save()

            # Update the MoistureTest instance
            moisture_test = form.save(commit=False)
            moisture_test.sample_a = sample_a  # Not necessary if sample_a hasn't changed
            moisture_test.sample_b = sample_b  # Not necessary if sample_b hasn't changed
            moisture_test.save()

            return redirect('laboratory:lab_assigned_samples')  # Redirect to success page
    else:
        # Pre-fill the form with the existing data
        form = MoistureTestForm(instance=moisture_test)

        if sample_a:
            form.fields['sample_a_empty_box_weight'].initial = str(sample_a.empty_box_weight).replace(',', '.')
            form.fields['sample_a_sample_weight_before_drying'].initial = str(
                sample_a.sample_weight_before_drying).replace(',', '.')
            form.fields['sample_a_sample_weight_after_drying'].initial = str(
                sample_a.sample_weight_after_drying).replace(',', '.')
            form.fields['result_a'].initial = str(sample_a.result).replace(',', '.')

        if sample_b:
            form.fields['sample_b_empty_box_weight'].initial = str(sample_b.empty_box_weight).replace(',', '.')
            form.fields['sample_b_sample_weight_before_drying'].initial = str(
                sample_b.sample_weight_before_drying).replace(',', '.')
            form.fields['sample_b_sample_weight_after_drying'].initial = str(
                sample_b.sample_weight_after_drying).replace(',', '.')
            form.fields['result_b'].initial = str(sample_b.result).replace(',', '.')

        # Setting oven temperature
        if moisture_test.oven_temperature is not None:
            form.fields['oven_temperature'].initial = moisture_test.oven_temperature

    return render(request, 'laboratory/create_moisture_test.html', {
        'form': form,
        'sample': assignment.sample,
    })


@login_required
def moisture_test_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample
    moisture_test = get_object_or_404(MoistureTest, assignment=assignment)

    # Retrieve related objects
    sample_a = moisture_test.sample_a
    sample_b = moisture_test.sample_b

    return render(request, 'laboratory/moisture_test_details.html', {
        'assignment': assignment,
        'sample': sample,
        'moisture_test': moisture_test,
        'sample_a': sample_a,
        'sample_b': sample_b,
    })

# -------------------------------------------------------------------------------------------------------------
