from django.db import models

from laboratory.models import Assignment


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
    empty_box_weight = models.FloatField(verbose_name='وزن العلبة  الفارغة')
    sample_weight_before_drying = models.FloatField(verbose_name='وزن العينة قبل التجفيف')
    sample_weight_after_drying = models.FloatField(verbose_name='وزن العينة بعد التجفيف')

    result = models.FloatField(verbose_name='الناتج')


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
    Category = models.CharField(max_length=100, verbose_name="اسم المحصول", default=' ')
    examination_method = models.CharField(max_length=100, choices=METHODS, verbose_name="طريقة الفحص ", null=True,
                                          blank=True)
    oven_temperature = models.FloatField(verbose_name=' درجة حرارة الفرن ', null=True, blank=True)
    number_of_drying_hours = models.FloatField(verbose_name='عدد ساعات التجفيف', null=True, blank=True)
    initial_weight = models.FloatField(verbose_name='الوزن قبل التجفيف', null=True, blank=True)
    unit_of_measure = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="وحدة القياس", null=True,
                                       blank=True)

    result_a = models.FloatField(verbose_name='ناتج العينة أ', null=True, blank=True)
    result_b = models.FloatField(verbose_name='ناتج العينة ب', null=True, blank=True)
    humidity = models.FloatField(verbose_name='نسبة الرطوبة النهائية')  # محتوى الرطوبة
    sample_a = models.ForeignKey(MoistureSample, on_delete=models.CASCADE, related_name='Moisture_tests_as_sample_a',
                                 limit_choices_to={'component_type': MoistureSample.sample_a}, null=True, blank=True)
    sample_b = models.ForeignKey(MoistureSample, on_delete=models.CASCADE, related_name='Moisture_tests_as_sample_b',
                                 limit_choices_to={'component_type': MoistureSample.sample_b}, null=True, blank=True)
    test_date = models.DateField(auto_now_add=True)  # Date when the test was conducted

    def __str__(self):
        return f"Moisture Test for {self.assignment.sample.sample_id}"

    class Meta:
        verbose_name = 'فحص الرطوبة'
        verbose_name_plural = 'فحوصات الرطوبة'