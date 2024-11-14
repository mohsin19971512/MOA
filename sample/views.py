from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from laboratory.Health.models import HealthTest
from laboratory.Moisture.models import MoistureTest
from laboratory.Plan.models import PlantTest
from laboratory.Purity.models import PurityTest
from .forms import SampleForm, HealthTestNotesForm
from laboratory.forms import AssignmentForm
from laboratory.models import Assignment
from laboratory.models import Lab
from django.db.models import Q
from django.shortcuts import render
from .models import Sample
from django.core.exceptions import ValidationError
from io import BytesIO
from weasyprint import HTML
from django.http import HttpResponse
from account.models import Profile
from itertools import zip_longest
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.core.paginator import Paginator
import logging
import os

import base64
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def get_file_content(file_path, max_size=10 * 1024 * 1024):  # 10MB limit
    """Safely read file content with size limit"""
    try:
        absolute_path = finders.find(file_path)
        if not absolute_path:
            logger.error(f"File not found: {file_path}")
            return None

        if os.path.getsize(absolute_path) > max_size:
            logger.error(f"File too large: {file_path}")
            return None

        with open(absolute_path, 'rb') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return None


def generate_certificate(request, sample_id):
    try:
        # Data for the certificate
        sample = Sample.objects.get(pk=sample_id)

        # Retrieve all assignments related to this sample
        assignments = Assignment.objects.filter(sample=sample)

        # Retrieve test results for each assignment
        health_tests = HealthTest.objects.filter(assignment__in=assignments).first()
        purity_tests = PurityTest.objects.filter(assignment__in=assignments).first()
        moisture_tests = MoistureTest.objects.filter(assignment__in=assignments).first()
        plant_tests = PlantTest.objects.filter(assignment__in=assignments).first()

        insect_examinations = []
        fungal_examinations = []
        nematode_tests = None

        if health_tests:
            if health_tests.insect_examinations.exists():
                insect_examinations = health_tests.insect_examinations.all()

            if health_tests.fungal_examinations.exists():
                fungal_examinations = health_tests.fungal_examinations.all()

            if health_tests.nematode_tests.exists():
                nematode_tests = health_tests.nematode_tests.all().first()
        else:
            print("health_tests is None")

        combined_examinations = zip_longest(insect_examinations, fungal_examinations, fillvalue=None)
        font_content = get_file_content('fonts/Cairo-VariableFont_slnt,wght.ttf')
        if font_content:
            font_base64 = base64.b64encode(font_content).decode('utf-8')
        else:
            font_base64 = None
            logger.warning("Failed to load Cairo font")

        # Load images
        logo_content = get_file_content('images/cert-logo.png')
        if logo_content:
            logo_base64 = base64.b64encode(logo_content).decode('utf-8')
        else:
            logo_base64 = None
            logger.warning("Failed to load cert logo")

        iqas_content = get_file_content('images/iqas2.png')
        if iqas_content:
            iqas_base64 = base64.b64encode(iqas_content).decode('utf-8')
        else:
            iqas_base64 = None
            logger.warning("Failed to load IQAS logo")

        # Your existing data preparation
        sample = Sample.objects.get(pk=sample_id)
        # ... rest of your data preparation ...

        # Prepare context with embedded assets
        context = {
            'font_base64': font_base64,
            'logo_base64': logo_base64,
            'iqas_base64': iqas_base64,
            'health_tests': health_tests,
            'moisture_tests': moisture_tests,
            'purity_tests': purity_tests,
            'plant_tests': plant_tests,
            'sample': sample,
            'insect_examinations': insect_examinations,
            'fungal_examinations': fungal_examinations,
            'nematode_tests': nematode_tests,
            'combined_examinations': combined_examinations,
        }

        # Generate PDF
        template = render_to_string('sample/certificate_template.html', context)

        pdf_buffer = BytesIO()
        HTML(string=template).write_pdf(
            pdf_buffer,
            stylesheets=[],
            optimize_size=('fonts', 'images')
        )

        # Create response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
        return response

    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        raise






@login_required
def home(request):
    profile = Profile.objects.get(user=request.user)
    user_role = profile.user_role

    if user_role == 'Lab':
        lab = profile.lab
        # Count the number of uncompleted and completed assignments
        total_assignments = Assignment.objects.filter(lab=lab).count()
        uncompleted_assignments = Assignment.objects.filter(lab=lab, completed=False).count()
        completed_assignments = Assignment.objects.filter(lab=lab, completed=True).count()

        context = {
            'uncompleted_assignments': uncompleted_assignments,
            'completed_assignments': completed_assignments,
            'total_assignments': total_assignments,
        }

    elif user_role in 'Altarmiz Manager':
        # Count the number of samples and their statuses
        total_samples = Sample.objects.count()
        completed_samples = Sample.objects.filter(lab_status='منجزة').count()
        uncompleted_samples = Sample.objects.filter(lab_status='غير منجزة').count()

        context = {
            'total_samples': total_samples,
            'completed_samples': completed_samples,
            'uncompleted_samples': uncompleted_samples,
        }
    else:
        total_samples = Sample.objects.count()
        completed_received = Sample.objects.filter(crop_name__isnull=False).count()
        uncompleted_received= Sample.objects.filter(crop_name__isnull=True).count()
        context = {
            'total_samples': total_samples,
            'completed_received': completed_received,
            'uncompleted_received': uncompleted_received,
        }


    return render(request, 'home.html', context)





@login_required
def add_sample(request):
    if request.method == 'POST':
        sample_form = SampleForm(request.POST,user=request.user)
        assignment_form = AssignmentForm(request.POST)
        
        if sample_form.is_valid() :
            # Save the sample
            sample = sample_form.save()

            # Get the selected labs from the assignment form
            if assignment_form.is_valid():
                labs = assignment_form.cleaned_data['labs']
            
            # Create assignments for each selected lab
                for lab in labs:
                    Assignment.objects.create(
                        sample=sample,
                        lab=lab
                    )

            return redirect('sample:all_samples')  # Redirect to the page with all assignments
    else:
        sample_form = SampleForm(user=request.user)
        assignment_form = AssignmentForm()
    
    return render(request, 'sample/add_sample.html', {
        'sample_form': sample_form,
        'assignment_form': assignment_form
    })


@login_required
def update_sample(request, sample_id):
    sample = get_object_or_404(Sample, id=sample_id)

    # Get the labs currently assigned to the sample
    current_labs = Assignment.objects.filter(sample=sample).values_list('lab', flat=True)

    if request.method == 'POST':
        sample_form = SampleForm(request.POST, instance=sample,user=request.user)
        assignment_form = AssignmentForm(request.POST)

        if sample_form.is_valid():
            # Save the updated sample
            sample = sample_form.save()

            # Get the selected labs from the form
            if assignment_form.is_valid():
                new_labs = assignment_form.cleaned_data['labs']

            # Handle adding/removing assignments
                current_assignments = Assignment.objects.filter(sample=sample)
                current_labs = current_assignments.values_list('lab', flat=True)

                labs_to_remove = current_assignments.exclude(lab__in=new_labs)
                labs_to_remove.delete()

                for lab in new_labs:
                    if lab.id not in current_labs:
                        Assignment.objects.create(sample=sample, lab=lab)

            return redirect('sample:all_samples')
    else:
        sample_form = SampleForm(instance=sample,user=request.user)
        # Initialize assignment form with current labs
        assignment_form = AssignmentForm(initial={'labs': current_labs})

    return render(request, 'sample/add_sample.html', {
        'sample_form': sample_form,
        'assignment_form': assignment_form
    })

@login_required
def all_samples(request):
    query = Q()

    # Get filters from request
    sample_id = request.GET.get('sample_id')
    crop_name = request.GET.get('crop_name')
    variety = request.GET.get('variety')
    sample_type = request.GET.get('sample_type')
    test_date = request.GET.get('test_date')
    completed = request.GET.get('completed')
    lab = request.GET.get('lab')
    assigned_date = request.GET.get('assigned_date')
    distinguishing_marks = request.GET.get('distinguishing_marks')

    # Build query based on filters
    if sample_id:
        query &= Q(sample_id__icontains=sample_id)

    if distinguishing_marks:
        query &= Q(distinguishing_marks__icontains=distinguishing_marks)
    if crop_name:
        query &= Q(crop_name__icontains=crop_name)
    if variety:
        query &= Q(variety__icontains=variety)
    if sample_type:
        query &= Q(sample_type__icontains=sample_type)
    if test_date:
        query &= Q(test_date=test_date)
    if completed:
        if completed.lower() == 'yes':
            query &= Q(lab_status='منجزة')
        elif completed.lower() == 'no':
            query &= Q(lab_status='غير منجزة')
        else:
            raise ValidationError(f"Invalid value for completed field: {completed}")
    if lab:
        query &= Q(assignment__lab__id=lab)
    if assigned_date:
        query &= Q(assignment__assigned_date=assigned_date)

    # Fetch samples
    samples_list = Sample.objects.filter(query).distinct().order_by('-created_date')

    # Pagination
    paginator = Paginator(samples_list, 10)  # Show 10 samples per page
    page_number = request.GET.get('page')
    samples = paginator.get_page(page_number)

    labs = Lab.objects.all()  # To populate the dropdown
    if request.user.profile.user_role in 'Manager':

        return render(request, 'sample/all_samples.html', {'samples': samples, 'labs': labs})
    elif request.user.profile.user_role in 'Altarmiz':
        return render(request, 'sample/altarmiz_all_samples.html', {'samples': samples, 'labs': labs})
    else :
        return render(request, 'sample/applicant_all_samples.html', {'samples': samples, 'labs': labs})




class SampleDetailView(DetailView):
    model = Sample
    template_name = 'sample/sample_detail.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample = self.object

        # Retrieve all assignments related to this sample
        assignments = Assignment.objects.filter(sample=sample)

        # Retrieve test results for each assignment
        health_tests = HealthTest.objects.filter(assignment__in=assignments).first()
        purity_tests = PurityTest.objects.filter(assignment__in=assignments)
        moisture_tests = MoistureTest.objects.filter(assignment__in=assignments)
        plant_tests = PlantTest.objects.filter(assignment__in=assignments)
        insect_examinations = []
        fungal_examinations = []
        nematode_tests = None

        if health_tests:
            if health_tests.insect_examinations.exists():
                insect_examinations = health_tests.insect_examinations.all()
            if health_tests.fungal_examinations.exists():
                fungal_examinations = health_tests.fungal_examinations.all()
            if health_tests.nematode_tests.exists():
                nematode_tests = health_tests.nematode_tests.all().first()

        combined_examinations = zip_longest(insect_examinations, fungal_examinations, fillvalue=None)

        # Add the form for editing HealthTest notes
        if self.request.method == 'POST':
            context['notes_form'] = HealthTestNotesForm(self.request.POST, instance=health_tests)
        else:
            context['notes_form'] = HealthTestNotesForm(instance=health_tests)

        context.update({
            'assignments': assignments,
            'health_tests': health_tests,
            'purity_tests': purity_tests,
            'moisture_tests': moisture_tests,
            'plant_tests': plant_tests,
            'insect_examinations': insect_examinations,
            'fungal_examinations': fungal_examinations,
            'nematode_tests': nematode_tests,
            'combined_examinations': combined_examinations,
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the current Sample object

        # Fetch assignments related to this sample
        assignments = Assignment.objects.filter(sample=self.object)

        # Fetch the related health tests based on the assignments
        health_tests = HealthTest.objects.filter(assignment__in=assignments).first()

        form = HealthTestNotesForm(request.POST, instance=health_tests)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.request.path_info)  # Redirect to the same page after saving
        return self.get(request, *args, **kwargs)

@login_required
def delete_sample(request, sample_id):
    sample = get_object_or_404(Sample, id=sample_id)

    if request.method == 'POST':
        # Perform the delete action
        sample.delete()
        messages.success(request, f"Sample '{sample.crop_name}' has been successfully deleted.")
        return redirect('sample:all_samples')  # Redirect to the list of samples

    # If the request is GET, render a page or handle accordingly
    return redirect('sample:all_samples')  # Redirect back if not a POST request