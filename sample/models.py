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
    crop_name = models.CharField(max_length=100, verbose_name="اسم المحصول والصنف", null=True, blank=True)
    distinguishing_marks = models.CharField(max_length=200,null=True, blank=True, verbose_name="رقم الأرسالية " ) # unique
    sample_id = models.CharField(max_length=100, unique=True, verbose_name="رقم العينة (الرقم المختبري)" , null=True, blank=True ) #tarmiz unique and search on distinguishing_marks
    shipment_weight = models.FloatField(verbose_name="وزن الأرسالية")
    unit_of_measure = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="وحدة القياس" , null=True, blank=True)
    location = models.CharField(max_length=100, null=True,blank=True,verbose_name="الموقع (عائدية البذور) ")
    sender_name = models.CharField(max_length=200, verbose_name="الجهة المرسلة (أسم الشركة)")
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE, verbose_name="نوع العينة" , null=True, blank=True)
    the_draw = models.CharField(max_length=100, verbose_name=" القائم بالسحب " , null=True,blank=True)
    batch_number = models.CharField(max_length=100, choices=batch_type,verbose_name="نوع البذور ")
    received_date = models.DateField(verbose_name="تاريخ الاستلام" , null=True, blank=True)
    withdrawal_date = models.DateField(verbose_name="تاريخ السحب" , null=True, blank=True)

    the_divider = models.CharField(max_length=100, verbose_name=" القائم بالتقسيم " , null=True,blank=True)
    test_date = models.DateField(verbose_name="تاريخ الفحص" , null=True, blank=True)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE, verbose_name= "نوع الفحص" , null=True, blank=True)
    purification_lab = models.CharField(max_length=200, verbose_name="معمل التنقية")
    result_date = models.DateField(verbose_name="تاريخ التبليغ ",null=True, blank=True,auto_now_add=True)
    lab_status = models.CharField(choices=LAB_STATUS, default='غير منجزة',max_length=100,null=True,blank=True,verbose_name="حالة المختبرات من الفحص")
    treatment_type = models.CharField(
        max_length=100,
        choices=TREATMENT_CHOICES,
        verbose_name="نوع المعاملة",
        null=True,blank=True,
    )
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.crop_name

    class Meta:
        verbose_name = "العينة"  # Singular name
        verbose_name_plural = "العينات"  # Plural name
    








