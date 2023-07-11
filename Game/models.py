from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Admin(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Guest(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_activated = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Country(models.Model):
    country_name = models.CharField(max_length=255)
    city_name = models.CharField(max_length=255)

    def __str__(self):
        return self.country_name + " " + self.city_name


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_done(self, request):
        user = request.user
        print(user)
        quiz = self.id
        done = QuizDone.objects.filter(quiz=quiz, user=user).count()
        if done >= 1:
            return True
        else:
            return False


class Answer(models.Model):
    name = models.CharField(max_length=255)
    is_country = models.BooleanField(default=False)
    is_true = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.name


class QuizDone(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
