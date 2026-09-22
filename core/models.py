from django.db import models
from django.core.exceptions import ValidationError

from users.models import CustomUser

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

        if not self.video_file and not self.iframe_url:
            raise ValidationError("You have to upload a video either its file or embed url")

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


class VideoAccess(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    max_views = models.PositiveBigIntegerField(null=True,blank=True,help_text="leave empty for unlimited access")
    views_used = models.PositiveBigIntegerField(default=0)

    def clean(self):
        super().clean()

        if self.max_views is None and not self.is_active:
            raise ValidationError(
                "Unlimited Video access must be active all the time"
            )
        if (self.max_views is not None and self.views_used > self.max_views):
            raise ValidationError(
                "Views used cannot exceed maximum views."
            )
    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student","video"],
                name="unique_student_video_access"
            )
        ]


# Teacher HW Submission
class Homework(models.Model):
    SUBMISSION_TYPES = [
        ("file", "File"),
        ("image", "Image"),
    ]
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="homeworks")
    title = models.CharField(max_length=255)
    submission_type = models.CharField(
        max_length=10,
        choices=SUBMISSION_TYPES
    )

#Student HW Submission
class HomeworkSubmission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submissions/files/",null=True,blank=True)
    image = models.ImageField(upload_to="submissions/images/",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.homework.submission_type == "file" and not self.file:
            raise ValidationError(
                "you must submit you homework file"
            )
        if self.homework.submission_type == "image" and not self.image:
            raise ValidationError(
                "you must submit you homework image"
            )

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name="exams")
    title = models.CharField(max_length=255)
    pass_percentage = models.PositiveIntegerField(default=60)

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    text = models.TextField()
    degree = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Progress(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    videos_watched = models.IntegerField(default=0)
    exam_passed = models.BooleanField(default=False)
    homework_done = models.BooleanField(default=False)


class ExamAttempt(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    score = models.IntegerField(default=0)

    is_submitted = models.BooleanField(default=False)
    percentage = models.FloatField(default=0)
    is_passed = models.BooleanField(default=False)
    class Meta:
        unique_together = ('student', 'exam')

class StudentAnswer(models.Model):
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE
    )

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('attempt', 'question')