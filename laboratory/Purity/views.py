from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from laboratory.Purity.forms import PurityTestForm, CropTypeCountForm, JungleCountForm
from laboratory.Purity.models import PurityTest
from laboratory.models import Assignment
from lov.models import Jungle, SampleWeight, SampleComponents, CropType, PurityTestCropType, PurityTestJungle


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

            return redirect(reverse('laboratory:purity_test_detail', args=[assignment_id]))  # Redirect to success page

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
            'pure_seeds_weight_a': str(pure_seeds_component.weight.weight_a).replace(',',
                                                                                     '.') if pure_seeds_component else '',
            'pure_seeds_weight_b': str(pure_seeds_component.weight.weight_b).replace(',',
                                                                                     '.') if pure_seeds_component else '',
            'inert_materials_weight_a': str(inert_materials_component.weight.weight_a).replace(',',
                                                                                               '.') if inert_materials_component else '',
            'inert_materials_weight_b': str(inert_materials_component.weight.weight_b).replace(',',
                                                                                               '.') if inert_materials_component else '',
            'other_seeds_weight_a': str(other_seeds_component.weight.weight_a).replace(',',
                                                                                       '.') if other_seeds_component else '',
            'other_seeds_weight_b': str(other_seeds_component.weight.weight_b).replace(',',
                                                                                       '.') if other_seeds_component else '',
            'weight_a': str(purity_test.weight.weight_a).replace(',', '.') if other_seeds_component else '',
            'weight_b': str(purity_test.weight.weight_b).replace(',', '.') if other_seeds_component else '',

        }

        # Set initial values in the form
        for field, value in initial_data.items():
            form.fields[field].initial = value

        # Prepare initial data for crop types
        crop_type_initial_data = {
            f'crop_type_{crop_type.id}': int(crop_type.count)
            for crop_type in purity_test.puritytestcroptype_set.all()
        }

        crop_type_form = CropTypeCountForm(initial=crop_type_initial_data, crop_types=CropType.objects.all())

        print("CropType Initial Data:", crop_type_form)
        for crop_type in purity_test.puritytestcroptype_set.all():
            print(f"Crop Type ID: {crop_type.id}, Count: {crop_type.count}")

        # Prepare initial data for jungles
        jungle_initial_data = {f'jungle_{jungle.id}': str(jungle.count).replace(',', '.') for jungle in
                               purity_test.puritytestjungle_set.all()}
        jungle_form = JungleCountForm(initial=jungle_initial_data, jungles=Jungle.objects.all())
        print("jungle_initial_data Initial Data:", jungle_initial_data)

    return render(request, 'laboratory/update_purity_test.html', {
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




