from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .Health.forms import HealthTestForm, InsectExaminationForm, FungalExaminationForm, BacterialExaminationForm, \
    NematodeTestForm, ViralTestForm
from .models import Assignment, MoistureTest, PlantTest,MoistureSample,SeedEntry
from .forms import PlantTestForm, SeedEntryForm,MoistureTestForm
from account.models import Profile
from django.db.models import Q,F, Sum,Value
from lov.models import SampleComponents, SampleWeight,CropType,Jungle,PurityTestCropType,PurityTestJungle
from django.urls import reverse
from django.db.models.functions import Coalesce

from django.shortcuts import redirect
from django.forms import formset_factory, inlineformset_factory


@login_required
def lab_assigned_samples(request):
    profile = Profile.objects.get(user=request.user)
    user_role = profile.user_role
    if user_role == 'Lab':
        lab = profile.lab
        query = Q(lab=lab)

        # Retrieve the search parameters from the request
        sample_id = request.GET.get('sample_id')
        crop_name = request.GET.get('crop_name')
        variety = request.GET.get('variety')
        sample_type = request.GET.get('sample_type')
        received_date = request.GET.get('received_date')
        completed = request.GET.get('completed')

        # Apply filters based on the search parameters
        if sample_id:
            query &= Q(sample__sample_id__icontains=sample_id)
        if crop_name:
            query &= Q(sample__crop_name__icontains=crop_name)
        if variety:
            query &= Q(sample__variety__icontains=variety)
        if sample_type:
            query &= Q(sample__sample_type__icontains=sample_type)
        if received_date:
            query &= Q(sample__received_date=received_date)
        if completed:
            if completed.lower() == 'yes':
                query &= Q(completed=True)
            elif completed.lower() == 'no':
                query &= Q(completed=False)

        # Filter the assignments based on the constructed query
        assignments = Assignment.objects.filter(query).order_by('completed', 'id').distinct()

        return render(request, 'laboratory/lab_assigned_samples.html', {'assignments': assignments})
    elif user_role in ['Manager', 'Applicant']:
        # Redirect to a page that shows all assignments with options for Manager and Applicant roles
        return redirect('sample:all_samples')  # Make sure to define this view and URL pattern
    else:
        # Handle other roles or unauthorized access
        return redirect('unauthorized')  # Make sure to define this view and URL pattern





@login_required
def all_assignments(request):
    assignments = Assignment.objects.all()  # Fetch all assignments
    return render(request, 'laboratory/all_assignments.html', {'assignments': assignments})




from django.forms import modelformset_factory
from django.db import IntegrityError
InsectExaminationFormSet = formset_factory(InsectExaminationForm, extra=2)
FungalExaminationFormSet = formset_factory(FungalExaminationForm, extra=3)
@login_required
def create_health_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample

    if request.method == 'POST':
        health_test_form = HealthTestForm(request.POST)
        insect_examination_formset = InsectExaminationFormSet(request.POST, prefix='insect')
        fungal_examination_formset = FungalExaminationFormSet(request.POST, prefix='fungal')
        bacterial_examination_form = BacterialExaminationForm(request.POST)
        nematode_test_form = NematodeTestForm(request.POST)
        viral_test_form = ViralTestForm(request.POST)

        if (health_test_form.is_valid() and
                insect_examination_formset.is_valid() and
                fungal_examination_formset.is_valid() and
                bacterial_examination_form.is_valid() and
                nematode_test_form.is_valid() and
                viral_test_form.is_valid()):

            try:
                # Save the health test first
                health_test = health_test_form.save(commit=False)
                health_test.assignment = assignment
                assignment.completed = True
                health_test.save()
                assignment.save()

                # Save all insect examination forms if any field is filled
                for form in insect_examination_formset:
                    if form.has_changed():
                        insect_examination = form.save(commit=False)
                        insect_examination.health_test = health_test
                        insect_examination.save()

                # Save all fungal examination forms if any field is filled
                for form in fungal_examination_formset:
                    if form.has_changed():
                        fungal_examination = form.save(commit=False)
                        fungal_examination.health_test = health_test
                        fungal_examination.save()

                # Save bacterial examination if any field is filled
                if bacterial_examination_form.has_changed():
                    bacterial_examination = bacterial_examination_form.save(commit=False)
                    bacterial_examination.health_test = health_test
                    bacterial_examination.save()

                # Save nematode test if any field is filled
                if nematode_test_form.has_changed():
                    nematode_test = nematode_test_form.save(commit=False)
                    nematode_test.health_test = health_test
                    nematode_test.save()

                # Save viral test if any field is filled
                if viral_test_form.has_changed():
                    viral_test = viral_test_form.save(commit=False)
                    viral_test.health_test = health_test
                    viral_test.save()

                return redirect('laboratory:lab_assigned_samples')  # Ensure this name matches your URL configuration

            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                # Handle the error, e.g., show an error message or redirect
                return redirect('some_error_page')  # Adjust as needed

        else:
            # Print out form errors for debugging
            print("Health Test Form Errors:", health_test_form.errors)
            print("Insect Examination Formset Errors:", insect_examination_formset.errors)
            print("Fungal Examination Formset Errors:", fungal_examination_formset.errors)
            print("Bacterial Examination Form Errors:", bacterial_examination_form.errors)
            print("Nematode Test Form Errors:", nematode_test_form.errors)
            print("Viral Test Form Errors:", viral_test_form.errors)

    else:
        health_test_form = HealthTestForm()
        insect_examination_formset = InsectExaminationFormSet(prefix='insect')
        fungal_examination_formset = FungalExaminationFormSet(prefix='fungal')
        bacterial_examination_form = BacterialExaminationForm()
        nematode_test_form = NematodeTestForm()
        viral_test_form = ViralTestForm()

    context = {
        'health_test_form': health_test_form,
        'insect_examination_formset': insect_examination_formset,
        'fungal_examination_formset': fungal_examination_formset,
        'bacterial_examination_form': bacterial_examination_form,
        'nematode_test_form': nematode_test_form,
        'viral_test_form': viral_test_form,
        'sample': sample,
    }
    return render(request, 'laboratory/create_health_test.html', context)




#-------------------------------------------------------------------------------------------------------------------------




#-------------------------------------------------------------------------------------------------------------
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
                sample_a.empty_box_weight = form.cleaned_data.get('sample_a_empty_box_weight', sample_a.empty_box_weight)
                sample_a.sample_weight_before_drying = form.cleaned_data.get('sample_a_sample_weight_before_drying', sample_a.sample_weight_before_drying)
                sample_a.sample_weight_after_drying = form.cleaned_data.get('sample_a_sample_weight_after_drying', sample_a.sample_weight_after_drying)
                sample_a.result = form.cleaned_data.get('result_a', sample_a.result)
                sample_a.save()

            # Check if sample_b exists before updating
            if sample_b:
                sample_b.empty_box_weight = form.cleaned_data.get('sample_b_empty_box_weight', sample_b.empty_box_weight)
                sample_b.sample_weight_before_drying = form.cleaned_data.get('sample_b_sample_weight_before_drying', sample_b.sample_weight_before_drying)
                sample_b.sample_weight_after_drying = form.cleaned_data.get('sample_b_sample_weight_after_drying', sample_b.sample_weight_after_drying)
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

#-------------------------------------------------------------------------------------------------------------





@login_required
def create_plant_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample
    total_value_1 = total_value_2 = total_value_3 = total_value_4 = total_value_5 = total_value_6 = total_value_7 = total_value_8 = 0

    # Try to get an existing PlantTest for this assignment
    plant_test = PlantTest.objects.filter(assignment_id=assignment_id).first()

    if request.method == 'POST':
        if plant_test:
            plant_test_form = PlantTestForm(request.POST, instance=plant_test)
            duplicates = plant_test.duplicates
        else:
            plant_test_form = PlantTestForm(request.POST)
            duplicates = '4x100'  # Or a default value if needed

        if plant_test_form.is_valid():
            plant_test = plant_test_form.save(commit=False)
            plant_test.assignment_id = assignment_id

            # Save plant_test before creating seed_entries
            plant_test.save()

            seed_entry_form = SeedEntryForm(request.POST, duplicates=duplicates)
            if seed_entry_form.is_valid():
                seed_entry = seed_entry_form.save(commit=False)
                seed_entry.plant_test = plant_test
                seed_entry.save()

                if 'add_another' not in request.POST:
                    # Set the Assignment as completed
                    assignment.completed = True
                    assignment.save()

                    # Calculate hard_percentage and natural_percentage
                    seed_entries = SeedEntry.objects.filter(plant_test=plant_test)

                    hard_sum = seed_entries.filter(seed_type='Hard').aggregate(
                        total_hard=Sum(
                            Coalesce(F('value_1'), Value(0)) + Coalesce(F('value_2'), Value(0)) +
                            Coalesce(F('value_3'), Value(0)) + Coalesce(F('value_4'), Value(0)) +
                            Coalesce(F('value_5'), Value(0)) + Coalesce(F('value_6'), Value(0)) +
                            Coalesce(F('value_7'), Value(0)) + Coalesce(F('value_8'), Value(0))
                        )
                    )['total_hard'] or 0

                    natural_sum = seed_entries.filter(seed_type='Natural').aggregate(
                        total_natural=Sum(
                            Coalesce(F('value_1'), Value(0)) + Coalesce(F('value_2'), Value(0)) +
                            Coalesce(F('value_3'), Value(0)) + Coalesce(F('value_4'), Value(0)) +
                            Coalesce(F('value_5'), Value(0)) + Coalesce(F('value_6'), Value(0)) +
                            Coalesce(F('value_7'), Value(0)) + Coalesce(F('value_8'), Value(0))
                        )
                    )['total_natural'] or 0

                    # Adjust calculation based on duplicates (4x100 or 8x50)
                    if duplicates == '4x100':
                        plant_test.hard_percentage = hard_sum / 4
                        plant_test.natural_percentage = natural_sum / 4
                    elif duplicates == '8x50':
                        plant_test.hard_percentage = hard_sum / 8
                        plant_test.natural_percentage = natural_sum / 8

                    # Save the updated PlantTest with percentages
                    plant_test.save()
                    return redirect(reverse('laboratory:create_plant_test', args=[assignment_id]))

                return redirect(reverse('laboratory:create_plant_test', args=[assignment_id]))
            else:
                print("Seed Entry Form Errors:", seed_entry_form.errors)
        else:
            print("Plant Test Form Errors:", plant_test_form.errors)
    else:
        if plant_test:
            plant_test_form = PlantTestForm(instance=plant_test)
            duplicates = plant_test.duplicates
            seed_entries = SeedEntry.objects.filter(plant_test=plant_test)

            # Calculate totals for each value field
            for entry in seed_entries:
                total_value_1 += entry.value_1 or 0
                total_value_2 += entry.value_2 or 0
                total_value_3 += entry.value_3 or 0
                total_value_4 += entry.value_4 or 0
                total_value_5 += entry.value_5 or 0
                total_value_6 += entry.value_6 or 0
                total_value_7 += entry.value_7 or 0
                total_value_8 += entry.value_8 or 0

            # Group by seed_type and calculate a total sum for all value fields combined
            seed_type_sums = seed_entries.values('seed_type').annotate(
                total_sum=Sum(
                    Coalesce(F('value_1'), Value(0)) + Coalesce(F('value_2'), Value(0)) +
                    Coalesce(F('value_3'), Value(0)) + Coalesce(F('value_4'), Value(0)) +
                    Coalesce(F('value_5'), Value(0)) + Coalesce(F('value_6'), Value(0)) +
                    Coalesce(F('value_7'), Value(0)) + Coalesce(F('value_8'), Value(0))
                )
            )
        else:
            plant_test_form = PlantTestForm()
            duplicates = '4x100'  # Or a default value if needed
            seed_entries = []
            seed_type_sums = []

        seed_entry_form = SeedEntryForm()
        print(seed_type_sums)

    return render(request, 'laboratory/create_plant_test.html', {
        'plant_test_form': plant_test_form,
        'plant_test': plant_test,
        'seed_entry_form': seed_entry_form,
        'sample': sample,
        'seed_entries': seed_entries,
        'total_value_1': total_value_1,
        'total_value_2': total_value_2,
        'total_value_3': total_value_3,
        'total_value_4': total_value_4,
        'total_value_5': total_value_5,
        'total_value_6': total_value_6,
        'total_value_7': total_value_7,
        'total_value_8': total_value_8,
        'seed_type_sums': seed_type_sums,  # Contains the sum of all values combined by seed_type
    })


@login_required
def update_plant_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample
    total_value_1 = total_value_2 = total_value_3 = total_value_4 = total_value_5 = total_value_6 = total_value_7 = total_value_8 = 0

    # Get the existing PlantTest
    plant_test = get_object_or_404(PlantTest, assignment_id=assignment_id)

    # Fetch the seed entries related to the plant test
    seed_entries = SeedEntry.objects.filter(plant_test=plant_test)

    # Initialize seed_type_sums
    seed_type_sums = []

    if request.method == 'POST':
        plant_test_form = PlantTestForm(request.POST, instance=plant_test)

        # Initialize formset and bind it to POST data
        SeedEntryFormSet = inlineformset_factory(PlantTest, SeedEntry, form=SeedEntryForm, extra=0, can_delete=True)
        seed_entries_formset = SeedEntryFormSet(request.POST, instance=plant_test, prefix='seed')

        if plant_test_form.is_valid() and seed_entries_formset.is_valid():
            # Save the updated PlantTest instance
            plant_test = plant_test_form.save(commit=False)
            plant_test.assignment_id = assignment_id
            plant_test.save()

            # Save the formset and handle updates to seed entries
            seed_entries_formset.save()

            # Recalculate totals for seed entries
            seed_entries = SeedEntry.objects.filter(plant_test=plant_test)
            hard_sum = seed_entries.filter(seed_type='Hard').aggregate(
                total_hard=Sum(
                    Coalesce(F('value_1'), Value(0)) + Coalesce(F('value_2'), Value(0)) +
                    Coalesce(F('value_3'), Value(0)) + Coalesce(F('value_4'), Value(0)) +
                    Coalesce(F('value_5'), Value(0)) + Coalesce(F('value_6'), Value(0)) +
                    Coalesce(F('value_7'), Value(0)) + Coalesce(F('value_8'), Value(0))
                )
            )['total_hard'] or 0

            natural_sum = seed_entries.filter(seed_type='Natural').aggregate(
                total_natural=Sum(
                    Coalesce(F('value_1'), Value(0)) + Coalesce(F('value_2'), Value(0)) +
                    Coalesce(F('value_3'), Value(0)) + Coalesce(F('value_4'), Value(0)) +
                    Coalesce(F('value_5'), Value(0)) + Coalesce(F('value_6'), Value(0)) +
                    Coalesce(F('value_7'), Value(0)) + Coalesce(F('value_8'), Value(0))
                )
            )['total_natural'] or 0

            # Adjust calculation based on duplicates (4x100 or 8x50)
            if plant_test.duplicates == '4x100':
                plant_test.hard_percentage = hard_sum / 4
                plant_test.natural_percentage = natural_sum / 4
            elif plant_test.duplicates == '8x50':
                plant_test.hard_percentage = hard_sum / 8
                plant_test.natural_percentage = natural_sum / 8

            # Save the updated PlantTest with percentages
            plant_test.save()

            return redirect(reverse('laboratory:update_plant_test', args=[assignment_id]))

        else:
            print("Form Errors:", plant_test_form.errors, seed_entries_formset.errors)

    else:
        # Pre-populate forms for an existing plant test
        plant_test_form = PlantTestForm(instance=plant_test)

        # Formsets for related models
        SeedEntryFormSet = inlineformset_factory(PlantTest, SeedEntry, form=SeedEntryForm, extra=0, can_delete=True)
        seed_entries_formset = SeedEntryFormSet(instance=plant_test, prefix='seed')

        # Calculate totals for each value field
        for entry in seed_entries:
            total_value_1 += entry.value_1 or 0
            total_value_2 += entry.value_2 or 0
            total_value_3 += entry.value_3 or 0
            total_value_4 += entry.value_4 or 0
            total_value_5 += entry.value_5 or 0
            total_value_6 += entry.value_6 or 0
            total_value_7 += entry.value_7 or 0
            total_value_8 += entry.value_8 or 0

        # Group by seed_type and calculate a total sum for all value fields combined
        seed_type_sums = seed_entries.values('seed_type').annotate(
            total_sum=Sum(
                Coalesce(F('value_1'), Value(0)) + Coalesce(F('value_2'), Value(0)) +
                Coalesce(F('value_3'), Value(0)) + Coalesce(F('value_4'), Value(0)) +
                Coalesce(F('value_5'), Value(0)) + Coalesce(F('value_6'), Value(0)) +
                Coalesce(F('value_7'), Value(0)) + Coalesce(F('value_8'), Value(0))
            )
        )

    return render(request, 'laboratory/update_plant_test.html', {
        'plant_test_form': plant_test_form,
        'plant_test': plant_test,
        'sample': sample,
        'seed_entries': seed_entries,
        'total_value_1': total_value_1,
        'total_value_2': total_value_2,
        'total_value_3': total_value_3,
        'total_value_4': total_value_4,
        'total_value_5': total_value_5,
        'total_value_6': total_value_6,
        'total_value_7': total_value_7,
        'total_value_8': total_value_8,
        'seed_type_sums': seed_type_sums,  # Contains the sum of all values combined by seed_type
        'seed_entries_formset': seed_entries_formset,  # Include the formset in the context
    })


