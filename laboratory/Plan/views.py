from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from laboratory.Plan.forms import PlantTestForm, SeedEntryForm
from laboratory.Plan.models import PlantTest, SeedEntry
from laboratory.models import Assignment
from django.db.models import Q,F, Sum,Value


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
                # Check if all fields are empty
                all_fields_empty = all(
                    seed_entry_form.cleaned_data.get(field, None) in [None, '', [], {}]
                    for field in seed_entry_form.fields
                )

                if not all_fields_empty:
                    seed_entry = seed_entry_form.save(commit=False)
                    seed_entry.plant_test = plant_test
                    seed_entry.save()

                if 'add_another' not in request.POST:
                    # Set the Assignment as completed
                    assignment.completed = True
                    assignment.save()

                    # if not all_fields_empty:
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
                        plant_test.hard_percentage = round(hard_sum / 4)
                        plant_test.natural_percentage = round(natural_sum / 4)
                    elif duplicates == '8x50':
                        plant_test.hard_percentage = round(hard_sum / 8)
                        plant_test.natural_percentage = round(natural_sum / 8)

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
        'assignment':assignment,
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
                plant_test.hard_percentage = round(hard_sum / 4)
                plant_test.natural_percentage = round(natural_sum / 4)
            elif plant_test.duplicates == '8x50':
                plant_test.hard_percentage = round(hard_sum / 8)
                plant_test.natural_percentage = round(natural_sum / 8)

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
