from django.db import models
from laboratory.models import Assignment


class HealthTest(models.Model):
    assignment = models.ForeignKey(Assignment,related_name='assing_health', on_delete=models.CASCADE, verbose_name='التعيين')
    note = models.TextField(verbose_name='ملاحظة', blank=True, null=True)
    test_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'اختبار الصحة'
        verbose_name_plural = 'اختبارات الصحة'

    def __str__(self):
        return f"اختبار الصحة في {self.test_date} لـ {self.assignment.lab}"


class InfectionType(models.Model):
    name = models.CharField(max_length=100, verbose_name='نوع الأصابة')

    class Meta:
        verbose_name = 'نوع الأصابة'
        verbose_name_plural = 'أنواع الأصابات'

    def __str__(self):
        return self.name



class Cause(models.Model):
    name = models.CharField(max_length=100, verbose_name=' المسبب')

    class Meta:
        verbose_name = 'المسبب '
        verbose_name_plural = ' المسببات'

    def __str__(self):
        return self.name

# Insect Examination
class InsectExamination(models.Model):
    health_test = models.ForeignKey(HealthTest, related_name='insect_examinations', on_delete=models.CASCADE, verbose_name='اختبار الصحة')
    infection_type = models.ForeignKey(InfectionType, on_delete=models.CASCADE, verbose_name='نوع الأصابة')
    infection_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='نسبة الأصابة')
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE, null=True,blank=True,verbose_name='المسبب ')

    class Meta:
        verbose_name = 'فحص الحشرات'
        verbose_name_plural = 'فحوصات الحشرات'

    def __str__(self):
        return f"فحص الحشرات: {self.infection_type} - {self.infection_percentage}%"


# Fungal Examination
class FungalExamination(models.Model):
    health_test = models.ForeignKey(HealthTest, related_name='fungal_examinations', on_delete=models.CASCADE, null=True,blank=True,verbose_name='اختبار الصحة')
    infection_percentage = models.DecimalField(null=True,blank=True,max_digits=5, decimal_places=2, verbose_name='نسبة الأصابة')
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE,null=True,blank=True, verbose_name='المسبب ') #text field

    class Meta:
        verbose_name = 'فحص الفطريات'
        verbose_name_plural = 'فحوصات الفطريات'

    def __str__(self):
        return f"فحص الفطريات: {self.infection_percentage}% - السبب: {self.cause.name}"


# Bacterial Examination
class BacterialExamination(models.Model):
    health_test = models.ForeignKey(HealthTest, related_name='bacterial_examinations', on_delete=models.CASCADE, null=True,blank=True,verbose_name='اختبار الصحة')
    infection_type = models.ForeignKey(InfectionType, on_delete=models.CASCADE, verbose_name='نوع الأصابة',null=True,blank=True)
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE,null=True,blank=True, verbose_name='المسبب ')
    damage_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='نسبة الضرر')
    greenness_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='نسبة الاخضرار')

    class Meta:
        verbose_name = 'فحص البكتيريا'
        verbose_name_plural = 'فحوصات البكتيريا'

    def __str__(self):
        return f"فحص البكتيريا - الضرر: {self.damage_percentage}%, الاخضرار: {self.greenness_percentage}%"


# Seed Health Test



# Nematode Test
class NematodeTest(models.Model):
    health_test = models.ForeignKey(HealthTest, related_name='nematode_tests', on_delete=models.CASCADE, verbose_name='اختبار الصحة')
    warts_count = models.IntegerField(verbose_name='عدد الأورام')

    class Meta:
        verbose_name = 'فحص الديدان'
        verbose_name_plural = 'فحوصات الديدان'

    def __str__(self):
        return f"فحص الديدان - عدد الأورام: {self.warts_count}"


# Viral Test
class ViralTest(models.Model):
    health_test = models.ForeignKey(HealthTest, related_name='viral_tests', on_delete=models.CASCADE, verbose_name='اختبار الصحة')
    infection_type = models.ForeignKey(InfectionType, on_delete=models.CASCADE, verbose_name='نوع الأصابة')
    infection_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='نسبة الأصابة')
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE,null=True,blank=True, verbose_name='المسبب ')

    class Meta:
        verbose_name = 'فحص الفيروسات'
        verbose_name_plural = 'فحوصات الفيروسات'

    def __str__(self):
        return f"فحص الفيروسات: {self.infection_type} - المعدل: {self.infection_rate}%"
