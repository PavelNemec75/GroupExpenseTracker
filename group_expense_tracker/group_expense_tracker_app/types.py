import strawberry
from strawberry import relay
from strawberry.relay import Connection
from strawberry.schema.types.base_scalars import Decimal

from . import models
from datetime import datetime
from typing import List, Optional


@strawberry.django.type(models.Event)
class EventType(relay.Node):
    id: relay.NodeID[str]  # noqa: A003
    name: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime

    @strawberry.field
    def event_participants(self) -> List["EventParticipantType"]:
        return models.EventParticipant.objects.filter(event_id=self.id)

    # @strawberry.field
    # def event_participants(self, event_id: Optional[str] = None) -> List["EventParticipantType"]:
    #     queryset = models.EventParticipant.objects.all()
    #     if event_id:
    #         queryset = queryset.filter(event_id=self.id)
    #     return queryset




@strawberry.django.type(models.Participant)
class ParticipantType(relay.Node):
    id: relay.NodeID[str]  # noqa: A003
    email: str
    first_name: str
    last_name: str
    created_at: datetime

    @strawberry.field
    def events(self) -> List["EventType"]:
        return models.Event.objects.filter(eventparticipant__participant_id=self.id)


@strawberry.django.type(models.EventParticipant)
class EventParticipantType(relay.Node):
    id: relay.NodeID[str]  # noqa: A003
    event: EventType
    participant: ParticipantType
    registered_at: datetime

    @strawberry.field
    def event_expense_group(self) -> List["EventExpenseGroupType"]:
        return models.EventExpenseGroup.objects.filter(event_participant_id=self.id)


@strawberry.django.type(models.EventExpenseItem)
class EventExpenseItemType(relay.Node):
    id: relay.NodeID[str]  # noqa: A003
    name: str
    price_eur: float


@strawberry.django.type(models.EventExpenseGroup)
class EventExpenseGroupType(relay.Node):
    id: relay.NodeID[str]  # noqa: A003
    paid_eur: float
    event_participant: EventParticipantType
    event_expense_item: EventExpenseItemType


@strawberry.type
class EventDataViewType:
    event_id: relay.NodeID[str]
    view_id: int
    event_name: str
    participant_id: int
    first_name: str
    last_name: str
    item_id: int
    item_name: str
    price: Decimal
    paid: Decimal
    balance: Decimal


@strawberry.type
class EventDataViewEdge:
    node: EventDataViewType
    cursor: str


@strawberry.type
class EventDataViewConnection(Connection):
    edges: List[EventDataViewEdge]
    page_info: relay.PageInfo
    total_count: int
