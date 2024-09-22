from django.db import models

from laboratory.models import Assignment
from lov.models import SampleWeight, SampleComponents


class PurityTest(models.Model):
    UNIT_CHOICES = [
        ('ton', 'طن'),
        ('kg', 'كيلوغرام'),
        ('gram', 'غرام'),
    ]
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE)
    Incoming_sample_weight = models.FloatField()
    unit_of_measure = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="وحدة القياس", null=True,
                                       blank=True)
    weight = models.ForeignKey(SampleWeight, on_delete=models.CASCADE,null=True,blank=True)
    pure_seeds = models.ForeignKey(SampleComponents, on_delete=models.CASCADE,
                                   related_name='purity_tests_as_pure_seeds',
                                   limit_choices_to={'component_type': SampleComponents.PURE_SEEDS}, null=True,
                                   blank=True)
    inert_materials = models.ForeignKey(SampleComponents, on_delete=models.CASCADE,
                                        related_name='purity_tests_as_inert_materials',
                                        limit_choices_to={'component_type': SampleComponents.INERT_MATERIALS},
                                        null=True, blank=True)
    other_seeds = models.ForeignKey(SampleComponents, on_delete=models.CASCADE,
                                    related_name='purity_tests_as_other_seeds',
                                    limit_choices_to={'component_type': SampleComponents.OTHER_SEEDS}, null=True,
                                    blank=True)
    purity_percentage = models.FloatField()
    inert_materials_percentage = models.FloatField()
    other_seeds_percentage = models.FloatField()
    test_date = models.DateField(auto_now_add=True)



    class Meta:
        verbose_name = 'اختبار النقاوة'
        verbose_name_plural = 'اختبارات النقاوة'

    def __str__(self):
        return f"اختبار النقاوة للعينة : {self.assignment.sample.sample_id}"