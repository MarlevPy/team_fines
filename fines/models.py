import operator
import datetime

from django.db import models
from django.contrib.auth.models import User


class Fine(models.Model):
    VIOLATIONS = {
        'late_training': ('Sen ankomst till träning', 30),
        'late_notice': ('Sen anmälan om missad träning', 30),
        'late_game': ('Sen ankomst till matchsamling', 50),
        'forgot_gear': ('Glömt material', 30),
        'wrong_gear': ('Felaktiga kläder på träning', 30),
        'stick_cutoff': ('Avslagen klubba', 100),
        'leave_training': ('Lämnat träning', 100),
        'penalty_2min': ('Utvisning 2min', 20),
        'penalty_5min': ('Utvisning 5min', 50),
        'shooting_during_brief': ('Skott under genomgång', 30),
        'forgot_shaker': ('Glömt skakers', 20),
        'pic_in_media': ('Bild i MVT/Corren', 20),
        'interview': ('Intervju i MVT/Corren', 30),
        'video_interview': ('Videointervju i MVT/Corren', 40),
        'interview_bollius': ('Intervjuad av Bollius', 20),
        'front_page': ('Framsida i tidningen', 50),
        'pic_nationwide_media': ('Bild i rikstäckande media', 30),
        'interview_nationwide_media': ('Intervju i rikstäckande media', 30),
    }

    VIOLATION_CHOICES = [(key, value[0]) for key, value in VIOLATIONS.items()]

    violation = models.CharField(max_length=255, choices=VIOLATION_CHOICES, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def amount(self):
        return self.VIOLATIONS.get(self.violation)[1]

    @property
    def violation_display(self):
        return self.get_violation_display()

    def __str__(self):
        return " | ".join([
            self.player.name,
            self.get_violation_display(),
            " ".join([str(self.amount), "kr"]),
            self.timestamp.strftime('%d/%m/%Y')
        ])


class Payment(models.Model):
    amount = models.DecimalField(max_digits=4, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return " | ".join([
            self.player.name,
            " ".join([str(self.amount), "kr"]),
            self.timestamp.strftime('%d/%m/%Y')
        ])


class Player(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user = models.ManyToManyField(User, related_name="player", blank=True)

    @property
    def name(self):
        return " ".join([str(self.first_name), str(self.last_name)])

    @property
    def name_lower(self):
        return self.name.lower()

    @property
    def payments(self):
        return self.payment_set.all()

    @property
    def payed(self):
        return sum([p.amount for p in self.payments])

    @property
    def fines(self):
        return self.fine_set.all()

    @property
    def fine_amount(self):
        return sum([f.amount for f in self.fines])

    @property
    def left_to_pay(self):
        return self.fine_amount - self.payed

    @property
    def num_fines(self):
        return len(self.fines)

    @property
    def num_payments(self):
        return len(self.payments)

    @property
    def history(self):
        payments = self.payments
        fines = self.fines
        history = sorted([i for i in payments] + [i for i in fines], key=operator.attrgetter("timestamp"), reverse=True)
        return history

    def __str__(self):
        return self.name
