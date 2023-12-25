from django.db import models


class Event(models.Model):
    name = models.TextField(blank=False, unique=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    email = models.EmailField(blank=False, unique=True)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class EventParticipant(models.Model):
    registered_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.participant} in {self.event}"


class EventExpenseGroup(models.Model):
    paid_eur = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    event_participant = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event_participant} - {self.event_expense_item}"


class EventExpenseItem(models.Model):
    name = models.TextField(blank=False)
    price_eur = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    event_expense_group = models.ForeignKey(EventExpenseGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
