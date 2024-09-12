from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SampleForm  # Import the form class
from laboratory.forms import AssignmentForm
from laboratory.models import Assignment
from .models import Sample
from laboratory.models import HealthTest,PlantTest,PurityTest,MoistureTest,Lab
from django.views.generic import DetailView
from django.db.models import Q
from django.shortcuts import render
from .models import Sample
from django.core.exceptions import ValidationError
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
import os
from django.conf import settings
from weasyprint import HTML
from django.http import HttpResponse






def generate_certificate(request):
    data = {
        'place': 'مسحوب',
        'applicant_name': 'اسم المتقدم',
        'sample_no': '1327',
        'sample_type': 'مسجلة',
        'date_of_test': '24/07/2024',
        'date_received': '24/07/2024',
        'lot_weight': '21',
        'variety_grade': 'باء 99',
        'purity': '96.33',
        'moisture': '6.90',
        'germination': '89',
        'nematoda_no': '2',
        'fungi_test': 'لايوجد',
        'insect_test': '12',
        'lab_manager': 'سالم طعمة كاصد',
    }

    template = get_template('sample/certificate_template.html')
    html = template.render(data)

    # Use the path from settings
    pdf_path = os.path.join(settings.TEMP_PDF_DIR, 'certificate.pdf')
    
    # Generate PDF and save to the path
    pdf_file = HTML(string=html).write_pdf(pdf_path)

    # Serve the PDF file in the response
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
        return response





@login_required
def home(request):
    return render(request, 'home.html')




@login_required
def add_sample(request):
    if request.method == 'POST':
        sample_form = SampleForm(request.POST)
        assignment_form = AssignmentForm(request.POST)
        
        if sample_form.is_valid() and assignment_form.is_valid():
            # Save the sample
            sample = sample_form.save()

            # Get the selected labs from the assignment form
            labs = assignment_form.cleaned_data['labs']
            
            # Create assignments for each selected lab
            for lab in labs:
                Assignment.objects.create(
                    sample=sample,
                    lab=lab
                )

            return redirect('sample:all_samples')  # Redirect to the page with all assignments
    else:
        sample_form = SampleForm()
        assignment_form = AssignmentForm()
    
    return render(request, 'sample/add_sample.html', {
        'sample_form': sample_form,
        'assignment_form': assignment_form
    })






@login_required
def all_samples(request):
    query = Q()

    sample_id = request.GET.get('sample_id')
    crop_name = request.GET.get('crop_name')
    variety = request.GET.get('variety')
    sample_type = request.GET.get('sample_type')
    test_date = request.GET.get('test_date')
    completed = request.GET.get('completed')
    lab = request.GET.get('lab')
    assigned_date = request.GET.get('assigned_date')

    if sample_id:
        query &= Q(sample_id__icontains=sample_id)
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
            query &= Q(assignment__completed=True)
        elif completed.lower() == 'no':
            query &= Q(assignment__completed=False)
        else:
            raise ValidationError(f"Invalid value for completed field: {completed}")
    if lab:
        query &= Q(assignment__lab__id=lab)
    if assigned_date:
        query &= Q(assignment__assigned_date=assigned_date)

    samples = Sample.objects.filter(query).distinct()
    labs = Lab.objects.all()  # To populate the dropdown
    return render(request, 'sample/all_samples.html', {'samples': samples, 'labs': labs})




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
        health_tests = HealthTest.objects.filter(assignment__in=assignments)
        purity_tests = PurityTest.objects.filter(assignment__in=assignments)
        moisture_tests = MoistureTest.objects.filter(assignment__in=assignments)
        plant_tests = PlantTest.objects.filter(assignment__in=assignments)
        print(plant_tests)
        
        

        context.update({
            'assignments': assignments,
            'health_tests': health_tests,
            'purity_tests': purity_tests,
            'moisture_tests': moisture_tests,
            'plant_tests': plant_tests,
        })
        return context
    


    