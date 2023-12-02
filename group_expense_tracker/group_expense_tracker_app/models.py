import uuid

from django.db import models, transaction


class Event(models.Model):
    event_id = models.TextField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    event_name = models.TextField(blank=False, unique=True)
    event_start_date = models.DateTimeField(null=True)
    event_end_date = models.DateTimeField(null=True)
    event_created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # expense_group_ids = EventExpenseGroup.objects.filter(
            #     event_participant__event=self).values_list('event_expense_group_id', flat=True,
            #                                                )
            # EventExpenseItem.objects.filter(event_expense_group__event_participant__event=self).delete()
            # EventExpenseItem.objects.filter(event_expense_item_id__in=event_expense_item_id).delete()
            # EventExpenseGroup.objects.filter(event_participant__event=self).delete()
            # EventParticipant.objects.filter(event=self).delete()
            super().delete(*args, **kwargs)
        return True

    def __str__(self):
        return self.event_name


class Participant(models.Model):
    participant_id = models.TextField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    participant_email = models.EmailField(blank=False, unique=True)
    participant_created_at = models.DateTimeField(auto_now_add=True)

    # def delete(self, *args, **kwargs):
    #     with transaction.atomic():
    #         expense_group_exists = EventExpenseGroup.objects.filter(
    #             event_participant__event=self,
    #         ).exists()
    #         if expense_group_exists:
    #             raise ValueError("Cannot delete Participant with associated EventExpenseGroup records.")
    #         # EventParticipant.objects.filter(participant=self).delete()
    #         super().delete(*args, **kwargs)
    #     return True

    def __str__(self):
        return self.participant_email


class EventParticipant(models.Model):
    event_participant_id = models.TextField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_participant_registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant} in {self.event}"


class EventExpenseItem(models.Model):
    event_expense_item_id = models.TextField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    event_expense_item_name = models.TextField(blank=False)
    event_expense_item_price_eur = models.DecimalField(blank=False, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.event_expense_item_name


class EventExpenseGroup(models.Model):
    event_expense_group_id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    event_participant = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    event_expense_item = models.ForeignKey(EventExpenseItem, on_delete=models.CASCADE)
    paid_eur = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.event_participant} - {self.event_expense_item}"
