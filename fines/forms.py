import operator

from django import forms
from django.db.utils import OperationalError

from .models import Fine, Player


class FineForm(forms.Form):
    player_choices = [('', '-'*20)]
    try:
        player_choices += sorted([(p.id, p.name) for p in Player.objects.all()], key=operator.itemgetter(1))
    except OperationalError:
        pass

    player = forms.ChoiceField(choices=player_choices, label='Spelare')

    violation_choices = [('', '-' * 20)]
    for key, value in Fine.VIOLATIONS.items():
        choice_text = f"{value[0]} ({value[1]} kr)"

        if key == 'interview_bollius':
            choice_text = f"{value[0]} (+{value[1]} kr)"

        violation_choices.append((key, choice_text))

    violation = forms.ChoiceField(choices=violation_choices, label='Överträdelse')


class RegisterPaymentForm(forms.Form):
    player_choices = [('', '-' * 20)]
    try:
        player_choices += sorted([(p.id, p.name) for p in Player.objects.all()], key=operator.itemgetter(1))
    except OperationalError:
        pass
    player = forms.ChoiceField(choices=player_choices, label='Spelare')

    amount = forms.DecimalField(max_digits=4, decimal_places=0, label='Belopp')


class RegisterSponsorForm(forms.Form):
    player_choices = [('', '-' * 20)]
    try:
        player_choices += sorted([(p.id, p.name) for p in Player.objects.all()], key=operator.itemgetter(1))
    except OperationalError:
        pass
    player = forms.ChoiceField(choices=player_choices, label='Spelare')

    amount = forms.DecimalField(max_digits=4, decimal_places=0, label='Belopp')
