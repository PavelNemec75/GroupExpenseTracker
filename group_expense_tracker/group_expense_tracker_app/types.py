import strawberry
from django.db.models import F
from strawberry import relay
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


@strawberry.django.type(models.Participant)
class ParticipantType(relay.Node):
    id: relay.NodeID[str]  # noqa: A003
    email: str
    first_name: str
    last_name: str
    created_at: datetime

    @strawberry.field
    def events(self) -> List["EventType"]:
        return models.Event.objects.filter(event_participant__participant_id=self.id)
    #
    # @strawberry.field
    # def expense_group(self) -> List["EventExpenseGroupType"]:
    #     return models.EventExpenseGroup.objects.filter(event_participant__participant_id=self.id)
    #
    # @strawberry.field
    # def expense_item(self) -> List["EventExpenseGroupType"]:
    #     return models.EventExpenseGroup.objects.filter(
    #         event_participant__participant_id=self.id)

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
