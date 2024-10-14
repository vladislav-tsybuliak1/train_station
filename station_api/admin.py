from django.contrib import admin

from station_api.models import (
    Station,
    Route,
    Crew,
    TrainType,
    Train,
    Trip,
    Ticket,
    Order,
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Trip)
admin.site.register(Ticket)
