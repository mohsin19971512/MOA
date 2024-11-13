from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assignment
from account.models import Profile
from django.db.models import Q,F, Sum,Value
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

        # Implement pagination
        paginator = Paginator(assignments, 10)  # Show 10 assignments per page
        page_number = request.GET.get('page')
        assignments_page = paginator.get_page(page_number)

        return render(request, 'laboratory/lab_assigned_samples.html', {'assignments': assignments_page})

    elif user_role in ['Manager', 'Applicant','Altarmiz']:
        # Redirect to a page that shows all assignments with options for Manager and Applicant roles
        return redirect('sample:all_samples')  # Make sure to define this view and URL pattern
    else:
        # Handle other roles or unauthorized access
        return redirect('unauthorized')  # Make sure to define this view and URL pattern








