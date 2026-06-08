from django.db import models

from core.models import Course
from users.models import CustomUser

# Create your models here.
class Payment(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ])

    method = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

