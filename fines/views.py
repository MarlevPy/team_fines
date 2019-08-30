import operator
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Player, Fine, Payment
from .forms import FineForm, RegisterPaymentForm


logger = logging.getLogger(__name__)


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('fines_index'))
    else:
        return render(request, 'index.html')


@login_required
def fines_index(request):
    players = sorted(Player.objects.all(), key=operator.attrgetter('last_name', 'first_name'))
    context = {
        'players': players,
        "fines_page": "active"
    }
    return render(request, 'fines_index.html', context)


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)

    context = {
        'player': player,
    }
    return render(request, 'player_detail.html', context)


def high_score(request):
    players = sorted(
        Player.objects.all(),
        key=operator.attrgetter('fine_amount', 'last_name', 'first_name'), reverse=True)
    context = {
        'players': players,
        "high_score_page": "active"
    }
    return render(request, 'high_score.html', context)


def new_fine(request):
    form = FineForm(request.POST or None)
    if form.is_valid():
        violation = request.POST.get('violation')
        player = get_object_or_404(Player, pk=request.POST.get('player'))
        create_another = bool(request.POST.get('create_another', False))

        fine = Fine.objects.create(violation=violation, player=player)

        if not create_another:
            return redirect('fines_index')
        else:
            messages.success(request, 'Ny böter tillagd.')

        logger.info(f'New fine added by {request.user}: {fine}')
    return render(request, 'new_fine.html', {'form': form})


def remove_fine(request, pk):
    fine = get_object_or_404(Fine, pk=pk)
    player = fine.player
    fine_description = str(fine)
    fine.delete()
    messages.add_message(request, messages.SUCCESS, 'Böter borttagen.')
    logger.info(f'Fine removed: {fine_description}')
    return render(request, 'player_detail.html', {'player': player})


def register_payment(request):
    form = RegisterPaymentForm(request.POST or None)
    if form.is_valid():
        player = get_object_or_404(Player, pk=request.POST.get('player'))
        amount = request.POST.get('amount')
        create_another = bool(request.POST.get('create_another', False))

        payment = Payment.objects.create(amount=amount, player=player)

        if not create_another:
            return redirect('fines_index')
        else:
            messages.success(request, 'Ny inbetalning tillagd.')
        logger.info(f'New paymenet registered:: {payment}')
    return render(request, 'register_payment.html', {'form': form})


def remove_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    player = payment.player
    payment_description = str(payment)
    payment.delete()
    messages.add_message(request, messages.SUCCESS, 'Inbetalning borttagen.')
    logger.info(f'Payment removed: {payment_description}')
    return render(request, 'player_detail.html', {'player': player})
