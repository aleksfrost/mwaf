from quiz.models import Users, Importance, Question, Quiz
from django import forms


class CareerAnchorForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)


        RATING_CHOISES = [(str(rate.value), str(rate.value)) for rate in Importance.objects.all()]

        self.fields["name"] = forms.CharField(
            min_length=1,
            required=True,
            label="Введите Ваше имя",
        )

        self.fields["email"] = forms.CharField(
            min_length=1,
            required=True,
            label="Введите Ваш email",
        )

        for question in questions:
            self.fields[f'question_{question.pk}'] = forms.ChoiceField(
                label=question.question,
                choices=RATING_CHOISES,
                widget=forms.RadioSelect(attrs={'class': 'horizontal-radios'})
            )

class StatsForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields["password"] = forms.CharField(
            min_length=6,
            required=True,
            label="Введите пароль",
        )



