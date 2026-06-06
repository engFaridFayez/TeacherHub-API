from django.db import models
from jsonschema import ValidationError

# Create your models here.
class Stage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Term(models.Model):
    name = models.CharField(max_length=255)
    stage = models.ForeignKey(Stage,on_delete=models.CASCADE,related_name="terms")

    def __str__(self):
        return f"{self.name} ل {self.stage}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    term = models.ForeignKey(Term,on_delete=models.CASCADE,related_name="courses")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Video(models.Model):
    VIDEO_TYPE_CHOICES = [
        ("file","uploaded File"),
        ("iframe","Iframe Embed")
    ]

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="videos")

    name = models.CharField(max_length=255)
    video_type = models.CharField(max_length=10,choices=VIDEO_TYPE_CHOICES)

        # لو فيديو مرفوع
    video_file = models.FileField(upload_to="courses/videos/", null=True, blank=True)

    # لو iframe (YouTube / Vimeo)
    iframe_url = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):

        super().clean()

        if self.video_type == "file" and not self.video_file:
            raise ValidationError("You must upload a video file")

        if self.video_type == "iframe" and not self.iframe_url:
            raise ValidationError("You must provide iframe url")

        if self.video_type == "file" and self.iframe_url:
            raise ValidationError("Remove iframe URL for file type")

        if self.video_type == "iframe" and self.video_file:
            raise ValidationError("Remove file for iframe type")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)