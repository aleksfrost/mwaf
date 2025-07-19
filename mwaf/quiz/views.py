
from collections import defaultdict
from django.db import IntegrityError, connection
from django.db.models import Avg
from django.db.models import F, Subquery, OuterRef
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import check_password

from .models import Anchor, Answer, Question, Quiz, Users
from .forms import CareerAnchorForm, StatsForm


def career_anchor(request: HttpRequest):

    quiz = Quiz.objects.get(quiz="Якоря карьеры")
    quiz_id = quiz.pk

    # Temporary limit 10 for debug
    questions = Question.objects.filter(quiz_id=quiz_id)

    if request.method == 'POST':
        form = CareerAnchorForm(request.POST, questions=questions)
        if form.is_valid():
            # Обработка результатов

            #User
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            new_user = Users(username=name, email=email)
            try:
                new_user.save()
            except IntegrityError:
                new_user = Users.objects.get(username=name, email=email)
            results = {}
            calc_results = defaultdict(list)
            for question in questions:
                field_name = f'question_{question.pk}'
                #results[question.pk] = form.cleaned_data[field_name]
                answer = Answer(user=new_user, question=question, value=form.cleaned_data[field_name])
                answer.save()
                calc_results[question.anchor.pk].append(form.cleaned_data[field_name])
                for key, values in calc_results.items():
                    values = [int(i) for i in values]
                    key = int(key)
                    anchor = Anchor.objects.get(pk=key).anchor
                    res = round(sum(values) / len(values), 1)
                    results[anchor] = res

            # Здесь можно сохранить результаты в базу
            return render(request, 'quiz/survey_results.html', {'results': results})
    else:
        form = CareerAnchorForm(questions=questions)


    return render(request, 'quiz/careeranchor.html', {'form': form})


def stats(request: HttpRequest):
    if request.method == 'POST':
        form = StatsForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            users = Users.objects.filter(is_admin=True)
            for user in users:
                is_valid = check_password("40летЧелябинска", user.password)
                if is_valid:
                    results = get_anchor_stats()
                    context = {
                        "stats": results,
                        "is_admin": True
                    }
                    return render(request, 'quiz/statistics.html', context)
    else:
        form = StatsForm()
    return render(request, 'quiz/statistics.html', {'form': form})


def get_anchor_stats():
    query = """
        SELECT
            u.username username,
            u.email email,
            qz.quiz quiz,
            a.passed_at passed_at,
            an.anchor anchor,
            avg(a.value) anchors_avg
        FROM answers a
        JOIN users u on a.user_id=u.id
        JOIN questions q on a.question_id=q.id
        JOIN anchors an on q.anchor_id=an.id
        JOIN quizes qz on q.quiz_id=qz.id
        GROUP BY u.username, q.anchor_id
        ORDER BY a.passed_at, u.username, qz.id;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

results = get_anchor_stats()