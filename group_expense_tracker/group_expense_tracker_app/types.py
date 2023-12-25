import strawberry
from strawberry import relay
from strawberry.relay import NodeType

from . import models
from datetime import datetime
from typing import Optional


@strawberry.django.type(models.Event, interfaces=[NodeType])
class EventType(relay.Node):
    id: relay.NodeID  # noqa: A003
    name: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime

    # @classmethod
    # def resolve_id(
    #     cls,
    #     root: models.Event,
    #     *,
    #     info: None,  # noqa: ARG003
    # ) -> str: return root.id
    #
    # @classmethod
    # def resolve_id_attr(cls) -> str:
    #     return "event_id"


@strawberry.django.type(models.Participant, interfaces=[NodeType])
class ParticipantType:
    id: relay.NodeID  # noqa: A003
    email: str
    first_name: str
    last_name: str
    created_at: datetime


@strawberry.django.type(models.EventParticipant, interfaces=[NodeType])
class EventParticipantType:
    id: relay.NodeID  # noqa: A003
    event: EventType
    participant: ParticipantType
    registered_at: datetime


@strawberry.django.type(models.EventExpenseGroup, interfaces=[NodeType])
class EventExpenseGroupType:
    id: relay.NodeID  # noqa: A003
    paid_eur: float
    event_participant: EventParticipantType


@strawberry.django.type(models.EventExpenseItem, interfaces=[NodeType])
class EventExpenseItemType:
    id: relay.NodeID  # noqa: A003
    name: str
    price_eur: float
    event_expense_item: EventExpenseGroupType
