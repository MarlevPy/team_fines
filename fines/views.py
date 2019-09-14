import operator
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

from background_task import background

from .models import Player, Fine, Payment
from .forms import FineForm, RegisterPaymentForm


logger = logging.getLogger(__name__)


@login_required
def index(request):
    fines = sorted(Fine.objects.all(), key=operator.attrgetter('timestamp'), reverse=True)[:10]
    player = request.user.player.first()

    if player and player.left_to_pay > 0:
        messages.warning(
            request,
            f'Du har {str(player.left_to_pay)} kr kvar att betala till böteskassan. '
            f'Se till att göra det så snart som möjligt.')

    context = {
        'player': player,
        'fines': fines,
        'sum_fines': get_total_fines_amount()
    }
    return render(request, 'index.html', context)


@login_required
def players_list(request):
    players = sorted(Player.objects.all(), key=operator.attrgetter('last_name', 'first_name'))
    context = {
        'players': players,
        'fines_page': 'active',
        'sum_fines': get_total_fines_amount()
    }
    return render(request, 'players_list.html', context)


@login_required
def fines_list(request):
    fines = list(Fine.VIOLATIONS.values())
    context = {
        'fines': fines,
        'sum_fines': get_total_fines_amount()
    }
    return render(request, 'fines_list.html', context)


@login_required
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    context = {
        'player': player,
        'sum_fines': get_total_fines_amount()
    }
    return render(request, 'player_detail.html', context)


@login_required
def high_score(request):
    players = sorted(
        Player.objects.all(),
        key=operator.attrgetter('fine_amount', 'last_name', 'first_name'), reverse=True)
    context = {
        'players': players,
        'high_score_page': 'active',
        'sum_fines': get_total_fines_amount()
    }
    return render(request, 'high_score.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='home')
def new_fine(request):
    form = FineForm(request.POST or None)
    if form.is_valid():
        violation = request.POST.get('violation')
        player = get_object_or_404(Player, pk=request.POST.get('player'))
        create_another = bool(request.POST.get('create_another', False))

        fine = Fine.objects.create(violation=violation, player=player, created_by=request.user)

        subject = '[SIBK Böter] - Ny bot'
        message = f'Hej, \nDu har åkt på en bot i vårt bötessystem i Solfjäderstadens IBK Herrlag. \n\nDen här gången har du åkt på {fine.violation_display} ({fine.amount} kr). \n\nBetala så snart som möjligt!. \n\nLäs mer under din användare på http://marlev89.pythonanywere.com/ \n\nVid problem av bötessidan. Hör av er till Levin.\n\n\nMvh \nBötessystemet'
        user = User.objects.filter(player=player)

        if user:
            email_to = user.first().email

            send_background_email(
                subject=subject,
                message=message,
                recipient_list=[email_to],
                sender=None,
            )

        messages.success(request, 'Ny böter tillagd.')
        logger.info(f'New fine added by {request.user}: {str(fine)}')

        if not create_another:
            return redirect('home')

    context = {
        'form': form,
        'title': 'Ny bot',
        'sum_fines': get_total_fines_amount()
    }

    return render(request, 'create_new.html', context)


@login_required
@user_passes_test(lambda u:u.is_staff, login_url='home')
def remove_fine(request, pk):
    fine = get_object_or_404(Fine, pk=pk)
    player = fine.player
    fine_description = str(fine)
    fine.delete()
    messages.add_message(request, messages.SUCCESS, 'Böter borttagen.')
    logger.info(f'Fine removed: {fine_description}')
    return render(request, 'player_detail.html', {'player': player})


@login_required
@user_passes_test(lambda u:u.is_staff, login_url='home')
def register_payment(request):
    form = RegisterPaymentForm(request.POST or None)
    if form.is_valid():
        player = get_object_or_404(Player, pk=request.POST.get('player'))
        amount = request.POST.get('amount')
        create_another = bool(request.POST.get('create_another', False))

        payment = Payment.objects.create(amount=amount, player=player, created_by=request.user)

        messages.success(request, 'Ny inbetalning tillagd.')
        logger.info(f'New paymenet registered:: {str(payment)}')

        if not create_another:
            return redirect('home')

    context = {
        'form': form,
        'title': 'Registrera betalning',
        'sum_fines': get_total_fines_amount()
    }

    return render(request, 'create_new.html', context)


@login_required
@user_passes_test(lambda u:u.is_staff, login_url='home')
def remove_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    player = payment.player
    payment_description = str(payment)
    payment.delete()
    messages.add_message(request, messages.SUCCESS, 'Inbetalning borttagen.')
    logger.info(f'Payment removed: {payment_description}')
    return render(request, 'player_detail.html', {'player': player})


@background(schedule=5)
def send_background_email(subject, message, recipient_list, sender=None):
    send_mail(subject, message, sender, recipient_list)
    logger.info(f'Sent email to: {recipient_list}.')


def get_total_fines_amount():
    return sum([f.amount for f in Fine.objects.all()])
