from django.db import models
from django.contrib.auth.models import User
from account.models import Profile
from sample.models import Sample
from lov.models import LabType,SampleComponents,SampleWeight

class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Lab name (e.g., Health, PurityTest)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)  # User responsible for this lab
    lab_type = models.ForeignKey(LabType,null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = ' المختبر'
        verbose_name_plural = ' المختبرات'

class Assignment(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)  # Sample assigned to the lab
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)  # Lab to which the sample is assigned
    assigned_date = models.DateField(auto_now_add=True)  # Date of assignment
    completed = models.BooleanField(default=False)  # Track if the lab has completed its testing

    def __str__(self):
        return f"   عينة رقم :  {self.sample.sample_id} الى {self.lab.name}"
    
    class Meta:
        verbose_name = 'تخصيص العينة الى المختبر '
        verbose_name_plural = 'تخصيصات العينات الى المختبرات '


