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









class MoistureSample(models.Model):
    sample_a = 'sample_a'
    sample_b = 'sample_b'
    COMPONENT_CHOICES = [
        (sample_a, 'عينة أ'),
        (sample_b, 'عينة ب'),
    ]

    component_type = models.CharField(
        max_length=50,
        choices=COMPONENT_CHOICES,
        default=sample_a,
    )
    empty_box_weight = models.FloatField( verbose_name='وزن العلبة  الفارغة') 
    sample_weight_before_drying = models.FloatField( verbose_name='وزن العينة قبل التجفيف') 
    sample_weight_after_drying = models.FloatField( verbose_name='وزن العينة بعد التجفيف') 

    result = models.FloatField( verbose_name='الناتج') 
    


class MoistureTest(models.Model):
    METHODS = [
        ('Oven', 'الفرن'),
        ('Khat ', 'الكت '),
    ]
    UNIT_CHOICES = [
        ('ton', 'طن'),
        ('kg', 'كيلوغرام'),
        ('gram', 'غرام'),
    ]

    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE)  # Link to the assignment
    Category = models.CharField(max_length=100, verbose_name="اسم المحصول",default=' ')
    examination_method = models.CharField(max_length=100,choices=METHODS,verbose_name="طريقة الفحص ",null=True, blank=True)
    oven_temperature = models.FloatField(verbose_name=' درجة حرارة الفرن ',null=True, blank=True)
    number_of_drying_hours =  models.FloatField(verbose_name='عدد ساعات التجفيف',null=True, blank=True)
    initial_weight = models.FloatField( verbose_name='الوزن قبل التجفيف',null=True, blank=True)
    unit_of_measure = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="وحدة القياس" , null=True, blank=True)

    result_a = models.FloatField( verbose_name='ناتج العينة أ',null=True, blank=True) 
    result_b = models.FloatField( verbose_name='ناتج العينة ب',null=True, blank=True) 
    humidity = models.FloatField(verbose_name='نسبة الرطوبة النهائية')  # محتوى الرطوبة
    sample_a = models.ForeignKey(MoistureSample, on_delete=models.CASCADE, related_name='Moisture_tests_as_sample_a', limit_choices_to={'component_type': MoistureSample.sample_a}, null=True, blank=True)
    sample_b = models.ForeignKey(MoistureSample, on_delete=models.CASCADE, related_name='Moisture_tests_as_sample_b', limit_choices_to={'component_type': MoistureSample.sample_b}, null=True, blank=True)
    test_date = models.DateField(auto_now_add=True)  # Date when the test was conducted

    def __str__(self):
        return f"Moisture Test for {self.assignment.sample.sample_id}"

    class Meta:
        verbose_name = 'فحص الرطوبة'
        verbose_name_plural = 'فحوصات الرطوبة'

# PlantTest model
class PlantTest(models.Model):
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE, null=True, blank=True)  # Link to the assignment
    DUPLICATE_CHOICES = [
        ('4x100', '4x100'),
        ('8x50', '8x50')
    ]
    
    SEED_CHOICES = [
        ('Natural', 'طبيعية'),
        ('Unnatural', 'غير طبيعية'),
        ('Hard', 'صلبة'),
        ('Dead', 'ميتة')
    ]
    
    number_of_seeds = models.PositiveIntegerField(verbose_name='عدد البذور', null=True, blank=True)
    temperature = models.DecimalField(verbose_name='درجة الحرارة',max_digits=5, decimal_places=2, null=True, blank=True)  # Storing temperature, e.g., 22.5°C
    planting_method = models.CharField(verbose_name='طريقة الزراعة',max_length=20, choices=[
        ('Roll', 'لف'),
        ('Fold', 'طي'),
        ('Sand', 'رمل')
    ], null=True, blank=True)
    tetrazonium_test = models.CharField(verbose_name='أختبار التترازوليوم',null=True,blank=True,max_length=50)
    seed_vitality = models.DecimalField(verbose_name='حيوية البذور',max_digits=5, decimal_places=2, null=True, blank=True)  # Percentage
    germination_power = models.DecimalField(verbose_name='قوة الأنبات',max_digits=5, decimal_places=2, null=True, blank=True)  # Percentage
    duplicates = models.CharField(verbose_name='التكرارات',max_length=5, choices=DUPLICATE_CHOICES, null=True, blank=True)
    hard_percentage = models.DecimalField(verbose_name='نسبة البذور الصلبة ',max_digits=5, decimal_places=2, null=True, blank=True) 
    natural_percentage = models.DecimalField(verbose_name='نسبة البذور الطبيعية ',max_digits=5, decimal_places=2, null=True, blank=True) 

    def __str__(self):
        return f"PlantTest {self.id} - {self.duplicates}"
    
    class Meta:
        verbose_name = 'اختبار الأنبات'
        verbose_name_plural = 'اختبارات الأنبات'


class SeedEntry(models.Model):
    plant_test = models.ForeignKey(PlantTest, on_delete=models.CASCADE, related_name='seed_entries', null=True, blank=True)
    seed_type = models.CharField(max_length=20, choices=PlantTest.SEED_CHOICES ,null=True, blank=True)
    count_date = models.DateField(null=True, blank=True)  # Date when the test was conducted

    value_1 = models.PositiveIntegerField(null=True, blank=True)
    value_2 = models.PositiveIntegerField(null=True, blank=True)
    value_3 = models.PositiveIntegerField(null=True, blank=True)
    value_4 = models.PositiveIntegerField(null=True, blank=True)
    value_5 = models.PositiveIntegerField(null=True, blank=True)  # Only used if duplicates are 8x50
    value_6 = models.PositiveIntegerField(null=True, blank=True)  # Only used if duplicates are 8x50
    value_7 = models.PositiveIntegerField(null=True, blank=True)  # Only used if duplicates are 8x50
    value_8 = models.PositiveIntegerField(null=True, blank=True)  # Only used if duplicates are 8x50

    def __str__(self):
        return f"{self.seed_type} Entry for PlantTest {self.plant_test.id}"

