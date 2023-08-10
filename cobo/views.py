from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'cobo/question_list.html', context)

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'cobo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)  # 이미지 업로드 처리를 위해 request.FILES 추가
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()

            # 이미지 처리 로직 추가
            image = request.FILES.get('image')  # 이미지 파일 가져오기
            if image:
                question.image = image

            question.save()
            return redirect(reverse('cobo:detail', kwargs={'question_id': question.pk}))
    else:
        form = QuestionForm()
    return render(request, 'cobo/question_form.html', {'form': form})

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES)  # 이미지 업로드 처리를 위해 request.FILES 추가
        if form.is_valid(): 
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question

            # 이미지 처리 로직 추가
            image = request.FILES.get('image')  # 이미지 파일 가져오기
            if image:
                answer.image = image

            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('cobo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'cobo/question_detail.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('cobo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('cobo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'cobo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('cobo:detail', question_id=question.id)
    question.delete()
    return redirect('cobo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question 
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('cobo:detail', question_id=answer.question.id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            
            image = request.FILES.get('image')  # 이미지 파일 가져오기
            if image:
                answer.image = image
            
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('cobo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'cobo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('cobo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('cobo:detail', question_id=question.id)


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question 
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(resolve_url('cobo:detail', question_id=question.id), answer.id))


