from django.db import models
from django.contrib.auth.models import User
from lov.models import LabType

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    user_role = models.CharField(max_length=50, choices=[
        ('Lab', 'مختبر'),
        ('Manager', 'مدير'),
        ('Applicant', 'شعبة التقسيم والخزن'),
        ('Altarmiz', 'شعبة  الترميز'),

    ], verbose_name='دور المستخدم')  # Assigning the user to a specific lab
    name = models.CharField(null=True, blank=True, max_length=150, verbose_name='الاسم')
    lab_type = models.ForeignKey(LabType, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='نوع المختبر')

    def __str__(self):
        return f"{self.user.username} - {self.user_role}"

    class Meta:
        verbose_name = 'الملف الشخصي'
        verbose_name_plural = 'الملفات الشخصية'




    
