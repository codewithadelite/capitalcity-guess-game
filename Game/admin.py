from django.contrib import admin
from .models import User, Admin, Guest, Country, Quiz, Answer, QuizDone

# Register your models here.

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Guest)
admin.site.register(Country)
admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(QuizDone)
