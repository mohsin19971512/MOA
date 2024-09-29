from django.shortcuts import get_object_or_404, redirect, render
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from .models import HealthTest, InsectExamination, FungalExamination, BacterialExamination, NematodeTest, ViralTest
from .forms import HealthTestForm, InsectExaminationForm, FungalExaminationForm, BacterialExaminationForm, \
    NematodeTestForm, ViralTestForm
from django.views.generic import DetailView
from django.forms import formset_factory, inlineformset_factory

from ..models import Assignment


@login_required
@transaction.atomic  # Ensure all operations are atomic (either all succeed or none)
def update_health_test(request, assignment_id):
    # Get the Assignment instance
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Get the Health instance related to the Assignment
    health_test = get_object_or_404(HealthTest, assignment=assignment)

    # Formsets for related models
    InsectExaminationFormSet = inlineformset_factory(HealthTest, InsectExamination, form=InsectExaminationForm, extra=1,
                                                     can_delete=True)
    FungalExaminationFormSet = inlineformset_factory(HealthTest, FungalExamination, form=FungalExaminationForm, extra=1,
                                                     can_delete=True)

    if request.method == 'POST':
        health_test_form = HealthTestForm(request.POST, instance=health_test)
        insect_examination_formset = InsectExaminationFormSet(request.POST, instance=health_test, prefix='insect')
        fungal_examination_formset = FungalExaminationFormSet(request.POST, instance=health_test, prefix='fungal')
        bacterial_examination_form = BacterialExaminationForm(request.POST,
                                                              instance=health_test.bacterial_examinations.first())
        nematode_test_form = NematodeTestForm(request.POST, instance=health_test.nematode_tests.first())
        viral_test_form = ViralTestForm(request.POST, instance=health_test.viral_tests.first())

        if (health_test_form.is_valid() and
                insect_examination_formset.is_valid() and
                fungal_examination_formset.is_valid() and
                bacterial_examination_form.is_valid() and
                nematode_test_form.is_valid() and
                viral_test_form.is_valid()):

            health_test_form.save()

            # Save all related formsets
            insect_examination_formset.save()
            fungal_examination_formset.save()

            # Save single instances if they exist
            if bacterial_examination_form.has_changed():
                bacterial_examination = bacterial_examination_form.save(commit=False)
                bacterial_examination.health_test = health_test
                bacterial_examination.save()

            if nematode_test_form.has_changed():
                nematode_test = nematode_test_form.save(commit=False)
                nematode_test.health_test = health_test
                nematode_test.save()

            if viral_test_form.has_changed():
                viral_test = viral_test_form.save(commit=False)
                viral_test.health_test = health_test
                viral_test.save()

            return redirect('laboratory:lab_assigned_samples')  # Redirect to a relevant page

        else:
            # Print form errors for debugging
            print("Health Test Form Errors:", health_test_form.errors)
            print("Insect Examination Formset Errors:", insect_examination_formset.errors)
            print("Fungal Examination Formset Errors:", fungal_examination_formset.errors)
            print("Bacterial Examination Form Errors:", bacterial_examination_form.errors)
            print("Nematode Test Form Errors:", nematode_test_form.errors)
            print("Viral Test Form Errors:", viral_test_form.errors)

    else:
        health_test_form = HealthTestForm(instance=health_test)
        insect_examination_formset = InsectExaminationFormSet(instance=health_test, prefix='insect')
        fungal_examination_formset = FungalExaminationFormSet(instance=health_test, prefix='fungal')
        bacterial_examination_form = BacterialExaminationForm(instance=health_test.bacterial_examinations.first())
        nematode_test_form = NematodeTestForm(instance=health_test.nematode_tests.first())
        viral_test_form = ViralTestForm(instance=health_test.viral_tests.first())

    context = {
        'health_test_form': health_test_form,
        'insect_examination_formset': insect_examination_formset,
        'fungal_examination_formset': fungal_examination_formset,
        'bacterial_examination_form': bacterial_examination_form,
        'nematode_test_form': nematode_test_form,
        'viral_test_form': viral_test_form,
        'sample': assignment.sample,
    }
    return render(request, 'laboratory/create_health_test.html', context)







# views.py

class HealthTestDetailView(DetailView):
    template_name = 'laboratory/health_test_detail.html'
    context_object_name = 'health_test'

    def get_object(self):
        assignment_id = self.kwargs.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        # Assuming there's only one Health per Assignment; adjust if necessary
        health_test = get_object_or_404(HealthTest, assignment=assignment)
        return health_test

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        health_test = self.get_object()
        assignment = health_test.assignment
        context['insect_examinations'] = health_test.insect_examinations.all()
        context['fungal_examinations'] = health_test.fungal_examinations.all()
        context['bacterial_examination'] = health_test.bacterial_examinations.first()
        context['nematode_test'] = health_test.nematode_tests.first()
        context['viral_test'] = health_test.viral_tests.first()
        context['sample'] = assignment.sample
        context['health_test'] = health_test
        return context





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
