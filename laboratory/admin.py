from django.contrib import admin

from laboratory.Health.models import HealthTest, InsectExamination, FungalExamination, BacterialExamination, \
    NematodeTest, ViralTest, Cause,InfectionType
from .Moisture.models import MoistureTest
from .Plan.models import PlantTest, SeedEntry
from .Purity.models import PurityTest
# Register your models here.
from .models import  Lab, Assignment

admin.site.register(Lab)
admin.site.register(Assignment)
admin.site.register(HealthTest)
admin.site.register(PurityTest)
admin.site.register(MoistureTest)
admin.site.register(PlantTest)
admin.site.register(SeedEntry)
admin.site.register(InsectExamination)

admin.site.register(FungalExamination)
admin.site.register(BacterialExamination)
admin.site.register(NematodeTest)
admin.site.register(ViralTest)
admin.site.register(InfectionType)

admin.site.register(Cause)
