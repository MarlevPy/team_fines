from django.contrib import admin
from fines.models import Player, Payment, Fine, Sponsor


class PlayerAdmin(admin.ModelAdmin):
    pass


class PaymentAdmin(admin.ModelAdmin):
    pass


class FineAdmin(admin.ModelAdmin):
    pass


class SponsorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Player, PlayerAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Fine, FineAdmin)
admin.site.register(Sponsor, SponsorAdmin)
