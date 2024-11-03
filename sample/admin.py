from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Sample
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("لوحة الإدارة")
admin.site.site_title = _("لوحة الإدارة")
admin.site.index_title = _("مرحبًا بك في لوحة الإدارة")
class SampleAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'sender_name', 'received_date', 'test_date', 'result_date')
    list_filter = ('sample_type', 'test_type', 'lab_status')
    search_fields = ('crop_name', 'sender_name', 'batch_number', 'sample_id')
    fieldsets = (
        (None, {
            'fields': ( 'sample_type', 'test_type')
        }),
        ('Sample Details', {
            'fields': ('crop_name', 'distinguishing_marks', 'sender_name', 'purification_lab', 'shipment_weight', 'batch_number', 'sample_id', 'treatment_type', 'lab_status')
        }),
        ('Dates', {
            'fields': ('received_date', 'test_date')
        }),
    )


admin.site.register(Sample, SampleAdmin)







