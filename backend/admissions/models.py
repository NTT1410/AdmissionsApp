from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class BaseModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)


class School(BaseModel):
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Hệ đào tạo
class Category(BaseModel):
    description = models.TextField(null=True, blank=True)
    duration = models.FloatField(default=0)
    requirements = models.TextField(null=True, blank=True)
    curriculum = models.TextField(null=True, blank=True)
    opportunities = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Thông tin tuyển sinnh
class Admissions(BaseModel):
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="admissions")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Department(BaseModel):
    introduction = models.TextField(null=True, blank=True)
    description = models.TextField()
    website = models.URLField(max_length=200, null=True, blank=True)
    video = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Score(BaseModel):
    description = models.TextField()
    image = models.ImageField(upload_to='images/scores/%Y/%m')


class Banner(BaseModel):
    image = models.ImageField(upload_to='images/banners/%Y/%m')
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name


class Stream(BaseModel):
    start_time = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(BaseModel):
    content = models.TextField()
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.content


class Answer(BaseModel):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")


class FAQ(BaseModel):
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admissions = models.ForeignKey(Admissions, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)


class Like(Interaction):
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'admissions')
