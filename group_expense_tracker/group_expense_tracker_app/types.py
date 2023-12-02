import strawberry
from . import models
from datetime import datetime
from typing import Optional


@strawberry.django.type(models.Event)
class EventType:
    event_id: str
    event_name: str
    event_start_date: Optional[datetime]
    event_end_date: Optional[datetime]
    event_created_at: datetime


@strawberry.django.type(models.Participant)
class ParticipantType:
    participant_id: str
    participant_email: str
    participant_created_at: datetime


@strawberry.django.type(models.EventParticipant)
class EventParticipantType:
    event_participant_id: str
    participant: ParticipantType
    event: EventType
    event_participant_registered_at: datetime


@strawberry.django.type(models.EventExpenseItem)
class EventExpenseItemType:
    event_expense_item_id: str
    event_expense_item_name: str
    event_expense_item_price_eur: float


@strawberry.django.type(models.EventExpenseGroup)
class EventExpenseGroupType:
    event_expense_group_id: str
    event_participant: EventParticipantType
    event_expense_item: EventExpenseItemType
    paid_eur: float
