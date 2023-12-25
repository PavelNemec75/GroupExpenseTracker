# from strawberry.types import Info
# from strawberry.utils.await_maybe import AwaitableOrValue
# from typing_extensions import Self

import strawberry
from strawberry import relay
from . import models
from datetime import datetime
from typing import List, Optional


@strawberry.django.type(models.Event)
class EventType(relay.Node):
    event_id: relay.NodeID[str]
    event_name: str
    event_start_date: Optional[datetime]
    event_end_date: Optional[datetime]
    event_created_at: datetime

    @classmethod
    def resolve_id(
        cls,
        root: models.Event,
        *,
        info: None,  # noqa: ARG003
    ) -> str: return root.event_id

    @classmethod
    def resolve_id_attr(cls) -> str:
        return "event_id"


@strawberry.django.type(models.Participant)
class ParticipantType:
    participant_id: str
    participant_email: str
    participant_first_name: str
    participant_last_name: str
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


@strawberry.type
class JoinedTypes:
    event: EventType
    participant: List[ParticipantType]
    event_participant: List[EventParticipantType]
    event_expense_item: List[EventExpenseItemType]
    event_expense_group: List[EventExpenseGroupType]
