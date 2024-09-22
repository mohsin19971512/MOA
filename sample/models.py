from random import choices

from django.db import models
from lov.models import CropType, Variety, Grade, SampleType, TestType





class Sample(models.Model):
    TREATMENT_CHOICES = [
        ('معفرة', 'معفرة'),
        ('غير معفرة', 'غير معفرة'),
    ]
    LAB_STATUS = [
        ('منجزة', 'منجزة'),
        ('غير منجزة', 'غير منجزة'),
    ]
    batch_type = [
        ('Big', 'كبيرة'),
        ('Small', 'صغيرة'),
    ]
    UNIT_CHOICES = [
        ('ton', 'طن'),
        ('kg', 'كيلوغرام'),
        ('gram', 'غرام'),
    ]
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE, verbose_name="نوع المحصول")
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, verbose_name="الصنف")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="الرتبة")
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE, verbose_name="نوع العينة")
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE, verbose_name="نوع الفحص")
    crop_name = models.CharField(max_length=100, verbose_name="اسم المحصول")
    distinguishing_marks = models.CharField(max_length=200,null=True, blank=True, verbose_name="رقم الأرسالية ")
    sender_name = models.CharField(max_length=200, verbose_name="الجهة المرسلة")
    purification_lab = models.CharField(max_length=200, verbose_name="معمل التنقية")
    sample_date = models.DateField(verbose_name="تاريخ سحب العينات")
    received_date = models.DateField(verbose_name="تاريخ الاستلام")
    test_date = models.DateField(verbose_name="تاريخ الفحص" , null=True, blank=True)
    result_date = models.DateField(verbose_name="تاريخ التبليغ ",null=True, blank=True,auto_now_add=True)
    shipment_weight = models.FloatField(verbose_name="وزن الأرسالية")
    unit_of_measure = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="وحدة القياس" , null=True, blank=True)

    batch_number = models.CharField(max_length=100, choices=batch_type,verbose_name="نوع البذور ")
    sample_id = models.CharField(max_length=100, unique=True, verbose_name="رقم العينة")
    lab_status = models.CharField(choices=LAB_STATUS, default='غير منجزة',max_length=100,null=True,blank=True,verbose_name="حالة المختبرات من الفحص")
    treatment_type = models.CharField(
        max_length=100,
        choices=TREATMENT_CHOICES,
        verbose_name="نوع المعاملة"
    )

    def __str__(self):
        return self.crop_name

    class Meta:
        verbose_name = "العينة"  # Singular name
        verbose_name_plural = "العينات"  # Plural name
    








