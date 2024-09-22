from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment

@receiver(post_save, sender=Assignment)
def check_all_assignments_completed(sender, instance, created, **kwargs):
    print('Signal Workinng')
    if not created:  # Only execute this code on update, not on creation
        sample = instance.sample
        all_assignments = Assignment.objects.filter(sample=sample)
        if all(assign.completed for assign in all_assignments):
            sample.lab_status = 'منجزة'
            sample.save()
            print('Signal Saved')










# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import PurityTest
# from lov.models import SampleComponents


# @receiver(post_save, sender=PurityTest)
# def create_sample_components(sender, instance, created, **kwargs):
#     if created:
#         # Check if `pure_seeds` should be created
#         if not instance.pure_seeds and instance.weight:
#             instance.pure_seeds = SampleComponents.objects.create(
#                 component_type=SampleComponents.PURE_SEEDS,
#                 weight=instance.weight
#             )
        
#         # Check if `inert_materials` should be created
#         if not instance.inert_materials and instance.weight:
#             instance.inert_materials = SampleComponents.objects.create(
#                 component_type=SampleComponents.INERT_MATERIALS,
#                 weight=instance.weight
#             )
        
#         # Check if `other_seeds` should be created
#         if not instance.other_seeds and instance.weight:
#             instance.other_seeds = SampleComponents.objects.create(
#                 component_type=SampleComponents.OTHER_SEEDS,
#                 weight=instance.weight
#             ) 
        
#         # Save the `PurityTest` instance after creating the components
#         instance.save()
