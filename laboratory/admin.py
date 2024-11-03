from django.contrib import admin

from laboratory.Health.models import HealthTest, InsectExamination, FungalExamination, BacterialExamination, \
    NematodeTest, ViralTest, Cause,InfectionType
from .Moisture.models import MoistureTest, MoistureSample
from .Plan.models import PlantTest, SeedEntry
from .Purity.models import PurityTest
# Register your models here.
from .models import  Lab, Assignment









class HealthTestAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'test_date', 'note')
    list_filter = ('test_date', 'assignment')
    search_fields = ('assignment__name',)


class InfectionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CauseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class InsectExaminationAdmin(admin.ModelAdmin):
    list_display = ('health_test', 'infection_type', 'infection_percentage', 'cause')
    list_filter = ('health_test', 'infection_type', 'cause')
    search_fields = ('health_test__assignment__name', 'infection_type__name', 'cause__name')


class FungalExaminationAdmin(admin.ModelAdmin):
    list_display = ('health_test', 'infection_percentage', 'cause')
    list_filter = ('health_test', 'cause')
    search_fields = ('health_test__assignment__name', 'cause__name')


class BacterialExaminationAdmin(admin.ModelAdmin):
    list_display = ('health_test', 'infection_type', 'damage_percentage', 'greenness_percentage', 'cause')
    list_filter = ('health_test', 'infection_type', 'cause')
    search_fields = ('health_test__assignment__name', 'infection_type__name', 'cause__name')


class NematodeTestAdmin(admin.ModelAdmin):
    list_display = ('health_test', 'warts_count')
    list_filter = ('health_test',)
    search_fields = ('health_test__assignment__name',)


class ViralTestAdmin(admin.ModelAdmin):
    list_display = ('health_test', 'infection_type', 'infection_rate', 'cause')
    list_filter = ('health_test', 'infection_type', 'cause')
    search_fields = ('health_test__assignment__name', 'infection_type__name', 'cause__name')


class MoistureSampleAdmin(admin.ModelAdmin):
    list_display = (
    'component_type', 'empty_box_weight', 'sample_weight_before_drying', 'sample_weight_after_drying', 'result')
    list_filter = ('component_type',)
    search_fields = ('component_type',)


class MoistureTestAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'Category', 'examination_method', 'test_date', 'initial_weight', 'humidity')
    list_filter = ('examination_method', 'test_date', 'Category')
    search_fields = ('assignment__sample__sample_id', 'Category')
    raw_id_fields = ('sample_a', 'sample_b')




class PlantTestAdmin(admin.ModelAdmin):
    list_display = (
    'assignment', 'number_of_seeds', 'temperature', 'planting_method', 'tetrazonium_test', 'seed_vitality',
    'germination_power', 'duplicates', 'agriculture_date')
    list_filter = ('planting_method', 'duplicates', 'agriculture_date')
    search_fields = ('assignment__sample__sample_id', 'tetrazonium_test')


class SeedEntryAdmin(admin.ModelAdmin):
    list_display = (
    'plant_test', 'seed_type', 'count_date', 'value_1', 'value_2', 'value_3', 'value_4', 'value_5', 'value_6',
    'value_7', 'value_8')
    list_filter = ('seed_type', 'count_date')
    search_fields = ('plant_test__id', 'seed_type')
    raw_id_fields = ('plant_test',)



class PurityTestAdmin(admin.ModelAdmin):
    list_display = (
    'assignment', 'Incoming_sample_weight', 'unit_of_measure', 'purity_percentage', 'inert_materials_percentage',
    'other_seeds_percentage', 'test_date')
    list_filter = ('test_date', 'unit_of_measure')
    search_fields = ('assignment__sample__sample_id',)
    raw_id_fields = ('weight', 'pure_seeds', 'inert_materials', 'other_seeds')




class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('sample', 'lab', 'assigned_date', 'completed')
    list_filter = ('assigned_date', 'completed', 'lab')
    search_fields = ('sample__sample_id', 'lab__name')
    date_hierarchy = 'assigned_date'  # Adds date hierarchy on assigned_date field for better navigation


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(HealthTest, HealthTestAdmin)
admin.site.register(InfectionType, InfectionTypeAdmin)
admin.site.register(Cause, CauseAdmin)
admin.site.register(InsectExamination, InsectExaminationAdmin)
admin.site.register(FungalExamination, FungalExaminationAdmin)
admin.site.register(BacterialExamination, BacterialExaminationAdmin)
admin.site.register(NematodeTest, NematodeTestAdmin)
admin.site.register(ViralTest, ViralTestAdmin)
admin.site.register(MoistureSample, MoistureSampleAdmin)
admin.site.register(MoistureTest, MoistureTestAdmin)


admin.site.register(Lab)
admin.site.register(PurityTest, PurityTestAdmin)
admin.site.register(PlantTest, PlantTestAdmin)
admin.site.register(SeedEntry, SeedEntryAdmin)