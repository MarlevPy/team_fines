from django import forms
from django.db.utils import OperationalError

from .models import Fine, Player


class FineForm(forms.Form):
    player_choices = [('', '-'*20)]
    try:
        player_choices += [(p.id, p.name) for p in Player.objects.all()]
    except OperationalError:
        pass

    player = forms.ChoiceField(choices=player_choices)

    violation_choices = [('', '-'*20)] + [
        (key, f"{value[0]} ({value[1]} kr{'/min' if value[0] == 'Utvisning' else ''}) ") for key, value in Fine.VIOLATIONS.items()
    ]
    violation = forms.ChoiceField(choices=violation_choices)


class RegisterPaymentForm(forms.Form):
    player_choices = [('', '-' * 20)]
    try:
        player_choices += [(p.id, p.name) for p in Player.objects.all()]
    except OperationalError:
        pass
    player = forms.ChoiceField(choices=player_choices)

    amount = forms.DecimalField(max_digits=4, decimal_places=0)
