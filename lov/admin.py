from django.contrib import admin
from .models import CropType, Variety, Grade, SampleType, TestType ,PurityTestCropType, LabType,SampleComponents,SampleWeight,Jungle

# Register your models here.
admin.site.register(CropType)
admin.site.register(Variety)
admin.site.register(Grade)
admin.site.register(SampleType)
admin.site.register(TestType)
admin.site.register(LabType)
admin.site.register(SampleComponents)

admin.site.register(SampleWeight)
admin.site.register(PurityTestCropType)
admin.site.register(Jungle)


