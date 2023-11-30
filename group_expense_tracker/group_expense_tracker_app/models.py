from django.db import models


class Event(models.Model):
    event_id = models.TextField(primary_key=True, unique=True)
    event_name = models.TextField()
    event_start_date = models.DateTimeField(null=True)
    event_end_date = models.DateTimeField(null=True)
    event_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name


class Participant(models.Model):
    participant_id = models.TextField(primary_key=True, unique=True)
    participant_email = models.EmailField(unique=True)
    participant_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.participant_email


class EventParticipant(models.Model):
    event_participant_id = models.TextField(primary_key=True, unique=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_participant_registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant} in {self.event}"


class EventExpenseItem(models.Model):
    event_expense_item_id = models.TextField(primary_key=True, unique=True)
    event_expense_item_name = models.TextField()
    event_expense_item_price_eur = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.event_expense_item_name


class EventExpenseGroup(models.Model):
    event_expense_group_id = models.TextField(primary_key=True, unique=True)
    event_participant = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    event_expense_item = models.ForeignKey(EventExpenseItem, on_delete=models.CASCADE)
    paid_eur = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.event_participant} - {self.event_expense_item}"
