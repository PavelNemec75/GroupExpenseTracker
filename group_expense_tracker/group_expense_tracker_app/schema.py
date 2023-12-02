from datetime import datetime

import strawberry
from typing import List
from typing import Optional
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
    def create_event(
            self,
            event_name: str,
            event_start_date: Optional[datetime] = None,
            event_end_date: Optional[datetime] = None,
    ) -> EventType:
        existing_event = Event.objects.filter(event_name=event_name).first()
        if existing_event:
            raise ValueError(f"Event with name \"{event_name}\"already exists.")

        new_event = Event(
            event_name=event_name,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
        )
        new_event.save()

        return EventType(
            event_id=new_event.event_id,
            event_name=new_event.event_name,
            event_start_date=new_event.event_start_date,
            event_end_date=new_event.event_end_date,
            event_created_at=new_event.event_created_at,
        )

    @strawberry.mutation
    def create_participant(
            self,
            participant_email: str,
    ) -> ParticipantType:
        existing_participant = Participant.objects.filter(participant_email=participant_email).first()
        if existing_participant:
            raise ValueError(f"Participant with email address \"{participant_email}\" already exists.")

        new_participant = Participant(
            participant_email=participant_email,
        )
        new_participant.save()

        return ParticipantType(
            participant_created_at=new_participant.participant_created_at,
            participant_email=new_participant.participant_email,
            participant_id=new_participant.participant_id,
        )

    @strawberry.mutation
    def add_event_participant(self, event_id: str, participant_id: str) -> EventParticipantType:
        event = Event.objects.get(event_id=event_id)
        participant = Participant.objects.get(participant_id=participant_id)
        event_participant = EventParticipant(event=event, participant=participant)
        event_participant.save()
        return event_participant


schema = strawberry.Schema(query=Query, mutation=Mutation)
