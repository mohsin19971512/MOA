from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Assignment, HealthTest, PurityTest, MoistureTest, PlantTest,MoistureSample,SeedEntry
from .forms import HealthTestForm, PurityTestForm, MoistureTestForm, PlantTestForm, SeedEntryForm,PurityTestForm, PurityTestCropTypeForm,PurityTestJungleForm,CropTypeCountForm, JungleCountForm,FungalExaminationForm,MoistureTestForm
from account.models import Profile
from django.db.models import Q,F, Sum,Value
from .models import Sample,FungalExamination
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from lov.models import SampleComponents, SampleWeight,CropType,Jungle,PurityTestCropType,PurityTestJungle
from django.urls import reverse
from django.db.models.functions import Coalesce

from django.shortcuts import redirect

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



@login_required
def create_health_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample

    if request.method == 'POST':
        health_test_form = HealthTestForm(request.POST)
        fungal_exam_form = FungalExaminationForm(request.POST)
        
        if health_test_form.is_valid() and fungal_exam_form.is_valid():
            fungal_examination = fungal_exam_form.save()
            health_test = health_test_form.save(commit=False)
            health_test.assignment = assignment
            health_test.fungal_examination = fungal_examination
            assignment.completed = True
            assignment.save()
            health_test.save()
            return redirect('laboratory:lab_assigned_samples')
    else:
        health_test_form = HealthTestForm()
        fungal_exam_form = FungalExaminationForm()
    
    context = {
        'health_test_form': health_test_form,
        'fungal_exam_form': fungal_exam_form,
        'assignment': assignment,
        'sample': sample,
    }
    
    return render(request, 'laboratory/create_health_test.html', context)


#-------------------------------------------------------------------------------------------------------------------------

@login_required
def create_purity_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample

    if request.method == 'POST':
        form = PurityTestForm(request.POST)
        crop_type_form = CropTypeCountForm(request.POST, crop_types=CropType.objects.all())
        jungle_form = JungleCountForm(request.POST, jungles=Jungle.objects.all())

        if form.is_valid() and crop_type_form.is_valid() and jungle_form.is_valid():
            # Create the main sample weight instance
            weight_instance = SampleWeight.objects.create(
                weight_a=form.cleaned_data['weight_a'],
                weight_b=form.cleaned_data['weight_b']
            )

            # Create the PurityTest instance
            purity_test = form.save(commit=False)
            purity_test.assignment = assignment
            purity_test.weight = weight_instance
            purity_test.save()

            # Create SampleComponents for pure seeds if provided
            if form.cleaned_data['pure_seeds_weight_a'] and form.cleaned_data['pure_seeds_weight_b']:
                pure_seeds_weight = SampleWeight.objects.create(
                    weight_a=form.cleaned_data['pure_seeds_weight_a'],
                    weight_b=form.cleaned_data['pure_seeds_weight_b']
                )
                pure_seeds_component = SampleComponents.objects.create(
                    component_type=SampleComponents.PURE_SEEDS,
                    weight=pure_seeds_weight
                )
                purity_test.pure_seeds = pure_seeds_component

            # Create SampleComponents for inert materials if provided
            if form.cleaned_data['inert_materials_weight_a'] and form.cleaned_data['inert_materials_weight_b']:
                inert_materials_weight = SampleWeight.objects.create(
                    weight_a=form.cleaned_data['inert_materials_weight_a'],
                    weight_b=form.cleaned_data['inert_materials_weight_b']
                )
                inert_materials_component = SampleComponents.objects.create(
                    component_type=SampleComponents.INERT_MATERIALS,
                    weight=inert_materials_weight
                )
                purity_test.inert_materials = inert_materials_component

            # Create SampleComponents for other seeds if provided
            if form.cleaned_data['other_seeds_weight_a'] and form.cleaned_data['other_seeds_weight_b']:
                other_seeds_weight = SampleWeight.objects.create(
                    weight_a=form.cleaned_data['other_seeds_weight_a'],
                    weight_b=form.cleaned_data['other_seeds_weight_b']
                )
                other_seeds_component = SampleComponents.objects.create(
                    component_type=SampleComponents.OTHER_SEEDS,
                    weight=other_seeds_weight
                )
                purity_test.other_seeds = other_seeds_component

            # Save CropType related data
            for field_name in crop_type_form.cleaned_data:
                if field_name.startswith('crop_type_'):
                    try:
                        crop_type_id = field_name.split('_')[2]  # Adjusted to correctly extract ID
                        count = crop_type_form.cleaned_data[field_name]
                        if count:
                            crop_type_instance = CropType.objects.get(id=crop_type_id)
                            PurityTestCropType.objects.create(
                                purity_test=purity_test,
                                crop_type=crop_type_instance,
                                count=count
                            )
                    except CropType.DoesNotExist:
                        # Handle the case where the CropType does not exist
                        pass

            # Save Jungle related data
            for field_name in jungle_form.cleaned_data:
                if field_name.startswith('jungle_'):
                    try:
                        jungle_id = field_name.split('_')[1]  # Adjusted to correctly extract ID
                        count = jungle_form.cleaned_data[field_name]
                        if count:
                            jungle_instance = Jungle.objects.get(id=jungle_id)
                            PurityTestJungle.objects.create(
                                purity_test=purity_test,
                                jungle=jungle_instance,
                                count=count
                            )
                    except Jungle.DoesNotExist:
                        # Handle the case where the Jungle does not exist
                        pass

            # Save the PurityTest with the updated fields
            assignment.completed = True
            assignment.save()
            purity_test.save()

            return redirect('laboratory:lab_assigned_samples')  # Redirect to success page

    else:
        form = PurityTestForm()
        crop_type_form = CropTypeCountForm(crop_types=CropType.objects.all())
        jungle_form = JungleCountForm(jungles=Jungle.objects.all())

    return render(request, 'laboratory/create_purity_test.html', {
        'form': form,
        'sample': sample,
        'crop_type_form': crop_type_form,
        'jungle_form': jungle_form
    })




@login_required
def update_purity_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample
    purity_test = get_object_or_404(PurityTest, assignment=assignment)
    # Fetch the related SampleWeight and SampleComponents instances
    weight_instance = purity_test.weight
    pure_seeds_component = purity_test.pure_seeds
    inert_materials_component = purity_test.inert_materials
    other_seeds_component = purity_test.other_seeds

    if request.method == 'POST':
        form = PurityTestForm(request.POST, instance=purity_test)
        crop_type_form = CropTypeCountForm(request.POST, crop_types=CropType.objects.all())
        jungle_form = JungleCountForm(request.POST, jungles=Jungle.objects.all())

        if form.is_valid() and crop_type_form.is_valid() and jungle_form.is_valid():
            # Update the main sample weight instance
            weight_instance.weight_a = form.cleaned_data['weight_a']
            weight_instance.weight_b = form.cleaned_data['weight_b']
            weight_instance.save()

            # Update or create SampleComponents for pure seeds
            if form.cleaned_data['pure_seeds_weight_a'] and form.cleaned_data['pure_seeds_weight_b']:
                if not pure_seeds_component:
                    pure_seeds_component = SampleComponents(component_type=SampleComponents.PURE_SEEDS)
                    purity_test.pure_seeds = pure_seeds_component
                pure_seeds_component.weight.weight_a = form.cleaned_data['pure_seeds_weight_a']
                pure_seeds_component.weight.weight_b = form.cleaned_data['pure_seeds_weight_b']
                pure_seeds_component.weight.save()
                pure_seeds_component.save()

            # Update or create SampleComponents for inert materials
            if form.cleaned_data['inert_materials_weight_a'] and form.cleaned_data['inert_materials_weight_b']:
                if not inert_materials_component:
                    inert_materials_component = SampleComponents(component_type=SampleComponents.INERT_MATERIALS)
                    purity_test.inert_materials = inert_materials_component
                inert_materials_component.weight.weight_a = form.cleaned_data['inert_materials_weight_a']
                inert_materials_component.weight.weight_b = form.cleaned_data['inert_materials_weight_b']
                inert_materials_component.weight.save()
                inert_materials_component.save()

            # Update or create SampleComponents for other seeds
            if form.cleaned_data['other_seeds_weight_a'] and form.cleaned_data['other_seeds_weight_b']:
                if not other_seeds_component:
                    other_seeds_component = SampleComponents(component_type=SampleComponents.OTHER_SEEDS)
                    purity_test.other_seeds = other_seeds_component
                other_seeds_component.weight.weight_a = form.cleaned_data['other_seeds_weight_a']
                other_seeds_component.weight.weight_b = form.cleaned_data['other_seeds_weight_b']
                other_seeds_component.weight.save()
                other_seeds_component.save()

            # Update or create CropType related data
            PurityTestCropType.objects.filter(purity_test=purity_test).delete()
            for field_name in crop_type_form.cleaned_data:
                if field_name.startswith('crop_type_'):
                    try:
                        crop_type_id = field_name.split('_')[2]  # Adjusted to correctly extract ID
                        count = crop_type_form.cleaned_data[field_name]
                        if count:
                            crop_type_instance = CropType.objects.get(id=crop_type_id)
                            PurityTestCropType.objects.create(
                                purity_test=purity_test,
                                crop_type=crop_type_instance,
                                count=count
                            )
                    except CropType.DoesNotExist:
                        pass

            # Update or create Jungle related data
            PurityTestJungle.objects.filter(purity_test=purity_test).delete()
            for field_name in jungle_form.cleaned_data:
                if field_name.startswith('jungle_'):
                    try:
                        jungle_id = field_name.split('_')[1]  # Adjusted to correctly extract ID
                        count = jungle_form.cleaned_data[field_name]
                        if count:
                            jungle_instance = Jungle.objects.get(id=jungle_id)
                            PurityTestJungle.objects.create(
                                purity_test=purity_test,
                                jungle=jungle_instance,
                                count=count
                            )
                    except Jungle.DoesNotExist:
                        pass

            # Save the updated PurityTest instance
            assignment.completed = True
            assignment.save()
            purity_test.save()

            return redirect('laboratory:lab_assigned_samples')  # Redirect to success page

    else:
        form = PurityTestForm(instance=purity_test)
        
        # Prepare initial data for pure seeds, inert materials, and other seeds
        initial_data = {
            'pure_seeds_weight_a': str(pure_seeds_component.weight.weight_a).replace(',', '.') if pure_seeds_component else '',
            'pure_seeds_weight_b': str(pure_seeds_component.weight.weight_b).replace(',', '.') if pure_seeds_component else '',
            'inert_materials_weight_a': str(inert_materials_component.weight.weight_a).replace(',', '.') if inert_materials_component else '',
            'inert_materials_weight_b': str(inert_materials_component.weight.weight_b).replace(',', '.') if inert_materials_component else '',
            'other_seeds_weight_a': str(other_seeds_component.weight.weight_a).replace(',', '.') if other_seeds_component else '',
            'other_seeds_weight_b': str(other_seeds_component.weight.weight_b).replace(',', '.') if other_seeds_component else '',
            'weight_a': str(purity_test.weight.weight_a).replace(',', '.') if other_seeds_component else '',
            'weight_b': str(purity_test.weight.weight_b).replace(',', '.') if other_seeds_component else '',


        }

        # Set initial values in the form
        for field, value in initial_data.items():
            form.fields[field].initial = value
    
        # Prepare initial data for crop types
        crop_type_initial_data = {f'crop_type_{crop_type.id}': str(crop_type.count).replace(',', '.') for crop_type in purity_test.puritytestcroptype_set.all()}
        crop_type_form = CropTypeCountForm(initial=crop_type_initial_data, crop_types=CropType.objects.all())
        print("CropType Initial Data:", crop_type_initial_data)

        # Prepare initial data for jungles
        jungle_initial_data = {f'jungle_{jungle.id}': str(jungle.count).replace(',', '.') for jungle in purity_test.puritytestjungle_set.all()}
        jungle_form = JungleCountForm(initial=jungle_initial_data, jungles=Jungle.objects.all())
        print("jungle_initial_data Initial Data:", jungle_initial_data)


    return render(request, 'laboratory/create_purity_test.html', {
        'form': form,
        'sample': sample,
        'crop_type_form': crop_type_form,
        'jungle_form': jungle_form
    })




@login_required
def purity_test_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample
    purity_test = get_object_or_404(PurityTest, assignment=assignment)

    # Retrieve related objects
    sample_weight = purity_test.weight
    pure_seeds_component = purity_test.pure_seeds
    inert_materials_component = purity_test.inert_materials
    other_seeds_component = purity_test.other_seeds
    
    crop_types = PurityTestCropType.objects.filter(purity_test=purity_test)
    jungles = PurityTestJungle.objects.filter(purity_test=purity_test)
    print(sample_weight.weight_a)
    return render(request, 'laboratory/purity_test_details.html', {
        'assignment': assignment,
        'sample': sample,
        'purity_test': purity_test,
        'sample_weight': sample_weight,
        'pure_seeds_component': pure_seeds_component,
        'inert_materials_component': inert_materials_component,
        'other_seeds_component': other_seeds_component,
        'crop_types': crop_types,
        'jungles': jungles,
        
    })







#-------------------------------------------------------------------------------------------------------------

@login_required
def create_moisture_test(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    sample = assignment.sample

    if request.method == 'POST':
        form = MoistureTestForm(request.POST)

        if form.is_valid():
            # Create the MoistureSample instances for sample_a and sample_b
            sample_a = MoistureSample.objects.create(
                component_type='sample_a',
                empty_box_weight=form.cleaned_data['sample_a_empty_box_weight'],
                sample_weight_before_drying=form.cleaned_data['sample_a_sample_weight_before_drying'],
                sample_weight_after_drying=form.cleaned_data['sample_a_sample_weight_after_drying'],
                result=form.cleaned_data['result_a']
            )
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
            moisture_test.sample_a = sample_a
            moisture_test.sample_b = sample_b
            moisture_test.save()

            # Mark the assignment as completed
            assignment.completed = True
            assignment.save()

            return redirect('laboratory:lab_assigned_samples')  # Redirect to success page
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
            # Update the MoistureSample instances for sample_a and sample_b
            sample_a.empty_box_weight = form.cleaned_data['sample_a_empty_box_weight']
            sample_a.sample_weight_before_drying = form.cleaned_data['sample_a_sample_weight_before_drying']
            sample_a.sample_weight_after_drying = form.cleaned_data['sample_a_sample_weight_after_drying']
            sample_a.result = form.cleaned_data['result_a']
            sample_a.save()

            sample_b.empty_box_weight = form.cleaned_data['sample_b_empty_box_weight']
            sample_b.sample_weight_before_drying = form.cleaned_data['sample_b_sample_weight_before_drying']
            sample_b.sample_weight_after_drying = form.cleaned_data['sample_b_sample_weight_after_drying']
            sample_b.result = form.cleaned_data['result_b']
            sample_b.save()

            # Update the MoistureTest instance
            moisture_test = form.save(commit=False)
            moisture_test.sample_a = sample_a
            moisture_test.sample_b = sample_b
            moisture_test.save()

            return redirect('laboratory:lab_assigned_samples')  # Redirect to success page
    else:
        # Pre-fill the form with the existing data
        form = MoistureTestForm(instance=moisture_test)


        form.fields['sample_a_empty_box_weight'].initial = str(sample_a.empty_box_weight).replace(',', '.')
        form.fields['sample_a_empty_box_weight'].initial = str(sample_a.empty_box_weight).replace(',', '.')
        form.fields['sample_a_sample_weight_before_drying'].initial = str(sample_a.sample_weight_before_drying).replace(',', '.')
        form.fields['sample_a_sample_weight_after_drying'].initial = str(sample_a.sample_weight_after_drying).replace(',', '.')
        form.fields['result_a'].initial = str(sample_a.result).replace(',', '.')

        form.fields['sample_b_empty_box_weight'].initial = str(sample_b.empty_box_weight).replace(',', '.')
        form.fields['sample_b_sample_weight_before_drying'].initial = str(sample_b.sample_weight_before_drying).replace(',', '.')
        form.fields['sample_b_sample_weight_after_drying'].initial = str(sample_b.sample_weight_after_drying).replace(',', '.')
        form.fields['result_b'].initial = str(sample_b.result).replace(',', '.')
        # form.fields['oven_temperature'].initial = str(moisture_test.oven_temperature).replace(',', '.')
        form.fields['oven_temperature'].initial = moisture_test.oven_temperature

        print(f"Initial value for oven_temperature: {form.fields['oven_temperature'].initial}")



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

# @login_required
# def create_plant_test(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
    
#     # Get or create a PlantTest instance linked to this assignment
#     plant_test, created = PlantTest.objects.get_or_create(assignment=assignment)
#     if request.method == 'POST':
#         plant_test_form = PlantTestForm(request.POST, instance=plant_test)
#         seed_count_formset = SeedCountFormSet(request.POST, queryset=SeedCount.objects.filter(plant_test=plant_test))
        
#         if plant_test_form.is_valid() and seed_count_formset.is_valid():
#             plant_test_form.save()
#             seed_counts = seed_count_formset.save(commit=False)
#             for seed_count in seed_counts:
#                 seed_count.plant_test = plant_test
#                 seed_count.save()
#             return redirect('laboratory:lab_assigned_samples')  # Replace with your success URL
#     else:
#         plant_test_form = PlantTestForm(instance=plant_test)
#         seed_count_formset = SeedCountFormSet(queryset=SeedCount.objects.filter(plant_test=plant_test))
    
#     return render(request, 'laboratory/create_plant_test.html', {
#         'plant_test_form': plant_test_form,
#         'seed_count_formset': seed_count_formset,
#     })






# @login_required
# def create_plant_test(request, assignment_id):
#     if request.method == 'POST':
#         plant_test_form = PlantTestForm(request.POST)
#         if plant_test_form.is_valid():
#             plant_test = plant_test_form.save(commit=False)
#             plant_test.assignment_id = assignment_id
#             plant_test.save()

#             # Handle multiple seed entries
#             for seed_type in request.POST.getlist('seed_type'):
#                 duplicates = plant_test.duplicates
#                 seed_entry_form = SeedEntryForm(request.POST, duplicates=duplicates, prefix=seed_type)
#                 if seed_entry_form.is_valid():
#                     seed_entry = seed_entry_form.save(commit=False)
#                     seed_entry.plant_test = plant_test
#                     seed_entry.save()

#             return redirect('laboratory:lab_assigned_samples')  # Replace with your success URL
#     else:
#         plant_test_form = PlantTestForm()
#         seed_entry_forms = [SeedEntryForm(prefix=seed_type) for seed_type in PlantTest.SEED_CHOICES]

#     return render(request, 'laboratory/create_plant_test.html', {
#         'plant_test_form': plant_test_form,
#         'seed_entry_forms': seed_entry_forms,
#     })



# @login_required
# def create_plant_test(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     sample = assignment.sample
    
#     if request.method == 'POST':
#         plant_test_form = PlantTestForm(request.POST)
#         if plant_test_form.is_valid():
#             plant_test = plant_test_form.save(commit=False)
#             plant_test.assignment_id = assignment_id
#             plant_test.save()

#             duplicates = plant_test.duplicates
#             seed_entry_form = SeedEntryForm(request.POST, duplicates=duplicates)
#             if seed_entry_form.is_valid():
#                 seed_entry = seed_entry_form.save(commit=False)
#                 seed_entry.plant_test = plant_test
#                 seed_entry.save()

#                 if 'add_another' in request.POST:
#                     return redirect(reverse('laboratory:create_plant_test', args=[assignment_id]))

#                 return redirect('laboratory:lab_assigned_samples')  # Replace with your success URL
#             else:
#                 print("Seed Entry Form Errors:", seed_entry_form.errors)
#         else:
#             print("Plant Test Form Errors:", plant_test_form.errors)
#     else:
#         plant_test_form = PlantTestForm()
#         seed_entry_form = SeedEntryForm()

#     return render(request, 'laboratory/create_plant_test.html', {
#         'plant_test_form': plant_test_form,
#         'seed_entry_form': seed_entry_form,
#         'sample': sample
#     })








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
