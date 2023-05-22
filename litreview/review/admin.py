from django.contrib import admin
from .models import Ticket, Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "user", "time_created"]
    list_filter = ["title", "time_created"]
    search_fields = ["title", "description"]
    ordering = ["user", "time_created"]
    raw_id_fields = ["user"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["ticket", "rating", "user", "headline", "time_created"]
    list_filter = ["ticket", "time_created"]
    ordering = ["user", "rating"]
    raw_id_fields = ["user", "ticket"]
