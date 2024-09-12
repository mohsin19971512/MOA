from django.db import models

class CropType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم المحصول")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع المحصول"  # Singular name
        verbose_name_plural = "أنواع المحاصيل"  # Plural name

class Jungle(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم الدغل")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = " الدغل"  # Singular name
        verbose_name_plural = "أنواع الأدغال"  # Plural name


class Variety(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="الصنف")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع الصنف"  # Singular name
        verbose_name_plural = "أنواع الأصناف"  # Plural name


class Grade(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="الرتبة")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع الرتبة"  # Singular name
        verbose_name_plural = "أنواع الرتب"  # Plural name


class SampleType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نوع العينة")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع العينة"  # Singular name
        verbose_name_plural = "أنواع العينات"  # Plural name


class TestType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نوع الفحص")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع الفحص"  # Singular name
        verbose_name_plural = "أنواع الفحوصات"  # Plural name


class LabType(models.Model):
    TREATMENT_CHOICES = [
        ('HealthTest', 'HealthTest'),
        ('PurityTest', 'PurityTest'),
        ('MoistureTest', 'MoistureTest'),
        ('PlantTest', 'PlantTest'),


    ]
    name = models.CharField(max_length=100, unique=True, verbose_name=" أسم المختبر",null=True,blank=True)
    lab_type = models.CharField(
        max_length=100,
        choices=TREATMENT_CHOICES,
        verbose_name="نوع المختبر",
        null=True,blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = " المختبر"  
        verbose_name_plural = "المختبرات "  




class SampleWeight(models.Model):
    weight_a = models.FloatField()  # Weight A
    weight_b = models.FloatField()  # Weight B

    class Meta:
        verbose_name = 'وزن العينة'
        verbose_name_plural = 'أوزان العينات'

    def __str__(self):
        return f"Weight A: {self.weight_a}, Weight B: {self.weight_b}"

class SampleComponents(models.Model):
    PURE_SEEDS = 'pure_seeds'
    INERT_MATERIALS = 'inert_materials'
    OTHER_SEEDS = 'other_seeds'

    COMPONENT_CHOICES = [
        (PURE_SEEDS, 'Pure Seeds'),
        (INERT_MATERIALS, 'Inert Materials'),
        (OTHER_SEEDS, 'Other Seeds'),
    ]

    component_type = models.CharField(
        max_length=50,
        choices=COMPONENT_CHOICES,
        default=PURE_SEEDS,
    )
    weight = models.ForeignKey(SampleWeight, on_delete=models.CASCADE)  # Link to SampleWeight


    class Meta:
        verbose_name = 'مكونات العينة'
        verbose_name_plural = 'مكونات العينات'

    def __str__(self):
        return f"{self.get_component_type_display()} - Weight A: {self.weight.weight_a}, Weight B: {self.weight.weight_b}"









class PurityTestCropType(models.Model):
    purity_test = models.ForeignKey('laboratory.PurityTest', on_delete=models.CASCADE)
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('purity_test', 'crop_type')

    def __str__(self):
        return f"{self.crop_type.name} - {self.count}"

class PurityTestJungle(models.Model):
    purity_test = models.ForeignKey('laboratory.PurityTest', on_delete=models.CASCADE)
    jungle = models.ForeignKey(Jungle, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('purity_test', 'jungle')

    def __str__(self):
        return f"{self.jungle.name} - {self.count}"