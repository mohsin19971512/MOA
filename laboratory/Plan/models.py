from django.db import models

from laboratory.models import Assignment


class PlantTest(models.Model):
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE, null=True,
                                      blank=True)  # Link to the assignment
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
    temperature = models.DecimalField(verbose_name='درجة الحرارة', max_digits=5, decimal_places=2, null=True,
                                      blank=True)  # Storing temperature, e.g., 22.5°C
    planting_method = models.CharField(verbose_name='طريقة الزراعة', max_length=20, choices=[
        ('Roll', 'لف'),
        ('Fold', 'طي'),
        ('Sand', 'رمل')
    ], null=True, blank=True)
    tetrazonium_test = models.CharField(verbose_name='أختبار التترازوليوم', null=True, blank=True, max_length=50)
    seed_vitality = models.DecimalField(verbose_name='حيوية البذور', max_digits=5, decimal_places=2, null=True,
                                        blank=True)  # Percentage
    germination_power = models.DecimalField(verbose_name='قوة الأنبات', max_digits=5, decimal_places=2, null=True,
                                            blank=True)  # Percentage
    duplicates = models.CharField(verbose_name='التكرارات', max_length=5, choices=DUPLICATE_CHOICES, null=True,
                                  blank=True)
    hard_percentage = models.DecimalField(verbose_name='نسبة البذور الصلبة ', max_digits=5, decimal_places=2, null=True,
                                          blank=True)
    natural_percentage = models.DecimalField(verbose_name='نسبة البذور الطبيعية ', max_digits=5, decimal_places=2,
                                             null=True, blank=True)

    def __str__(self):
        return f"PlantTest {self.id} - {self.duplicates}"

    class Meta:
        verbose_name = 'اختبار الأنبات'
        verbose_name_plural = 'اختبارات الأنبات'


class SeedEntry(models.Model):
    plant_test = models.ForeignKey(PlantTest, on_delete=models.CASCADE, related_name='seed_entries', null=True,
                                   blank=True)
    seed_type = models.CharField(max_length=20, choices=PlantTest.SEED_CHOICES, null=True, blank=True)
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