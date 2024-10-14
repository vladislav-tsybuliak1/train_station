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

admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Trip)
admin.site.register(Ticket)
admin.site.register(Order)
