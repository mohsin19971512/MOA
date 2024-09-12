from django.contrib import admin

# Register your models here.
from .models import  Lab, Assignment, HealthTest, PurityTest, MoistureTest, PlantTest,SeedEntry

admin.site.register(Lab)
admin.site.register(Assignment)
admin.site.register(HealthTest)
admin.site.register(PurityTest)
admin.site.register(MoistureTest)
admin.site.register(PlantTest)
admin.site.register(SeedEntry)

