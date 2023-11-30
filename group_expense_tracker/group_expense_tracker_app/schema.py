import strawberry
from typing import List
from .models import Event, Participant, EventParticipant, EventExpenseItem, EventExpenseGroup
from .types import EventType, ParticipantType, EventParticipantType, EventExpenseItemType, EventExpenseGroupType


@strawberry.type
class Query:
    @strawberry.field
    def get_events(self) -> List[EventType]:
        return list(Event.objects.all())

    @strawberry.field
    def get_participants(self) -> List[ParticipantType]:
        return list(Participant.objects.all())

    @strawberry.field
    def get_event_participants(self) -> List[EventParticipantType]:
        return list(EventParticipant.objects.all())

    @strawberry.field
    def get_event_expense_items(self) -> List[EventExpenseItemType]:
        return list(EventExpenseItem.objects.all())

    @strawberry.field
    def get_event_expense_groups(self) -> List[EventExpenseGroupType]:
        return list(EventExpenseGroup.objects.all())


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_event(self, event_name: str) -> EventType:
        event = Event(event_name=event_name)
        event.save()
        return event

    @strawberry.mutation
    def create_participant(self, participant_email: str) -> ParticipantType:
        participant = Participant(participant_email=participant_email)
        participant.save()
        return participant

    @strawberry.mutation
    def add_event_participant(self, event_id: str, participant_id: str) -> EventParticipantType:
        event = Event.objects.get(event_id=event_id)
        participant = Participant.objects.get(participant_id=participant_id)
        event_participant = EventParticipant(event=event, participant=participant)
        event_participant.save()
        return event_participant


schema = strawberry.Schema(query=Query, mutation=Mutation)
