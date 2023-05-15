from django import forms
from .models import Quiz, Question,Answer,StudentFormq
from django.contrib import admin

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'description', 'number_of_questions', 'time')

    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('content', 'quiz')
        
class StudentForm(forms.ModelForm): 
    class Meta:  
        model = StudentFormq 
        fields = "__all__"