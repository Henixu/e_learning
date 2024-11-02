from django.contrib import admin
from .models import User, Category, Course, UserProgress, Quiz, QuizResult, Recommendation

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(UserProgress)
admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Recommendation)
