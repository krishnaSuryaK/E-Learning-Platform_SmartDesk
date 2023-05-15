from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm,StudentForm
from .models import *
from django.forms import inlineformset_factory
from django.contrib import messages
from django.http import HttpResponse
from .function import handle_uploaded_file_ai,handle_uploaded_file_dm,handle_uploaded_file_os,handle_uploaded_file_wt,handle_uploaded_file_mccp
import os


def notes(request):
    return render(request,"quiz/notes.html")

def displaypdf(request):
    return render(request,'quiz/sub.html')

def displaypdfmccp(request):
    path=(r"C:\Users\karth\OneDrive\Desktop\Poll-App (1)\quiz\static\upload\MCCP")
    pdf_list =os.listdir(path)   
    return render(request, 'quiz/MCCP_notes.html', {'pdfs': pdf_list})

def displaypdfdm(request):
    path=(r"C:\Users\karth\OneDrive\Desktop\Poll-App (1)\quiz\static\upload\DM")
    pdf_list =os.listdir(path)   
    return render(request, 'quiz/DM_notes.html', {'pdfs': pdf_list})

def displaypdfos(request):
    path=(r"C:\Users\karth\OneDrive\Desktop\Poll-App (1)\quiz\static\upload\OS")
    pdf_list =os.listdir(path)   
    return render(request, 'quiz/OS_notes.html', {'pdfs': pdf_list})

def displaypdfwt(request):
    path=(r"C:\Users\karth\OneDrive\Desktop\Poll-App (1)\quiz\static\upload\WT")
    pdf_list =os.listdir(path)   
    return render(request, 'quiz/WT_notes.html', {'pdfs': pdf_list})

def displaypdfai(request):
    path=(r"C:\Users\karth\OneDrive\Desktop\Poll-App (1)\quiz\static\upload\AI")
    pdf_list =os.listdir(path)   
    return render(request, 'quiz/AI_notes.html', {'pdfs': pdf_list})

def fileup(request):
    if request.user.has_perm('polls.add_poll'):
        if request.method == 'POST':  
            student = StudentForm(request.POST, request.FILES)  
            s1=request.POST['firstname']
            x=request.POST['subject']
            if student.is_valid():
                if x=='MCCP':
                    handle_uploaded_file_mccp(request.FILES['file'],s1)  
                    model_instance = student.save(commit=False)
                    model_instance.save()
                    return HttpResponse("File uploaded successfuly<br><a href='\'>BACK</a> ")
                elif x=='OS':
                    handle_uploaded_file_os(request.FILES['file'],s1)  
                    model_instance = student.save(commit=False)
                    model_instance.save()
                    return HttpResponse("File uploaded successfuly<br><a href='\'>BACK</a> ")
                elif x=='WT':
                    handle_uploaded_file_wt(request.FILES['file'],s1)  
                    model_instance = student.save(commit=False)
                    model_instance.save()
                    return HttpResponse("File uploaded successfuly<br><a href='\'>BACK</a> ")
                elif x=='AI':
                    handle_uploaded_file_ai(request.FILES['file'],s1)  
                    model_instance = student.save(commit=False)
                    model_instance.save()
                    return HttpResponse("File uploaded successfuly<br><a href='\'>BACK</a> ")
                elif x=='DM':
                    handle_uploaded_file_dm(request.FILES['file'],s1)  
                    model_instance = student.save(commit=False)
                    model_instance.save()
                    return HttpResponse("File uploaded successfuly<br><a href='\'>BACK</a> ")
                  
        else:  
            student=StudentForm()  
            return render(request,"quiz/fileupload.html",{'form':student})
    else:
        return HttpResponse("<div style='top:20px'><center><h2>Sorry but you don't have permission to do that!</h2> <a href='/'>go</a></center></div>")

def index(request):
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, "quiz/index.html", para)

@login_required
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz/quiz.html", {'quiz':quiz})

def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.content)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, myid):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                    else:
                        if a.correct:
                            correct_answer = a.content

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})
     
        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)
        
        return JsonResponse({'passed': True, 'score': score, 'marks': marks})

def add_quiz(request):
    if request.method=="POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            # obj = form.instance
            # return render(request, "quiz/add_quiz.html", {'obj':obj})
            return redirect('quiz:index')
    else:
        form=QuizForm()
    return render(request, "quiz/add_quiz.html", {'form':form})

def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quiz/add_question.html')
    else:
        form=QuestionForm()
    return render(request, "quiz/add_question.html", {'form':form, 'questions':questions})

def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    # if request.method == "POST":
    question.delete()
    return redirect('quiz:add_question')
    # return render(request, "quiz/delete_question.html", {'question':question})


def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "quiz/add_options.html", {'alert':alert})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "quiz/add_options.html", {'formset':formset, 'question':question})

def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "quiz/results.html", {'marks':marks})

def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    # if request.method == "POST":
    marks.delete()
    return redirect("quiz:results")
