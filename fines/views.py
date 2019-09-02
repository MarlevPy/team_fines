import operator
import logging
import threading

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

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
    fines = sorted(Fine.objects.all(), key=operator.attrgetter('timestamp'), reverse=True)[:10]
    player = request.user.player.first()

    if player.left_to_pay > 0:
        messages.warning(
            request,
            f'Du har {str(player.left_to_pay)} kr kvar att betala till böteskassan. '
            f'Se till att göra det så snart som möjligt.')

    context = {
        'player': player,
        'fines': fines
    }
    return render(request, 'fines_index.html', context)


@login_required
def players_list(request):
    players = sorted(Player.objects.all(), key=operator.attrgetter('last_name', 'first_name'))
    context = {
        'players': players,
        "fines_page": "active"
    }
    return render(request, 'players_list.html', context)


@login_required
def fines_list(request):
    fines = list(Fine.VIOLATIONS.values())
    return render(request, 'fines_list.html', {'fines': fines})


@login_required
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'player_detail.html', {'player': player})


@login_required
def high_score(request):
    players = sorted(
        Player.objects.all(),
        key=operator.attrgetter('fine_amount', 'last_name', 'first_name'), reverse=True)
    context = {
        'players': players,
        "high_score_page": "active"
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
        message = f'Hej, \nDu har åkt på en bot i vårt bötessystem i Solfjäderstadens IBK Herrlag. \n\nDen här gången har du åkt på {fine.violation_display} ({fine.amount} kr). \n\n Betala så snart som möjligt!. \n\n Läs mer under din användare på http://marlev89.pythonanywere.com/ \n\n\n Mvh \nBötessystemet.'
        email_to = User.objects.get(player=player).email

        send_threaded_mail(
            subject=subject,
            message=message,
            recipient_list=[email_to],
            sender=None,
        )

        if not create_another:
            return redirect('fines_index')
        else:
            messages.success(request, 'Ny böter tillagd.')

        logger.info(f'New fine added by {request.user}: {fine}')

    return render(request, 'new_fine.html', {'form': form})


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

        if not create_another:
            return redirect('fines_index')
        else:
            messages.success(request, 'Ny inbetalning tillagd.')
        logger.info(f'New paymenet registered:: {payment}')
    return render(request, 'register_payment.html', {'form': form})


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


class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list, sender=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.message = message
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(self.subject, self.message, self.sender, self.recipient_list)
        except TimeoutError:
            logger.error(f'Could not send mail to {self.recipient_list}.')


def send_threaded_mail(subject, message, recipient_list, sender=None):
    EmailThread(subject, message, recipient_list, sender).start()
