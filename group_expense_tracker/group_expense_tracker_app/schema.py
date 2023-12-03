from datetime import datetime

import strawberry
from typing import List
from typing import Optional
from .models import Event, Participant, EventParticipant, EventExpenseItem, EventExpenseGroup
from .types import EventType, ParticipantType, EventParticipantType, EventExpenseItemType, EventExpenseGroupType
from django.core.exceptions import ObjectDoesNotExist


@strawberry.type
class Query:

    @strawberry.field
    def get_events(self) -> List[EventType]:
        return list(Event.objects.all())

    @strawberry.field
    def get_participants(self) -> List[ParticipantType]:
        return list(Participant.objects.all())

    @strawberry.field
    def get_event_participants(
            self,
            event_id: str,
    ) -> List[EventParticipantType]:
        try:
            event = Event.objects.get(event_id=event_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Event with ID {event_id} does not exist.") from err

        participants = EventParticipant.objects.filter(event=event)
        return [EventParticipantType(
            # event_id=participant.event_id,
            # participant_id=participant.participant_id,
            event_participant_id=participant.event_participant_id,
            event=participant.event,
            participant=participant.participant,
            event_participant_registered_at=participant.event_participant_registered_at,

        ) for participant in participants]

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
    def delete_event(
            self,
            event_id: strawberry.ID,
    ) -> bool:
        try:
            event_to_delete = Event.objects.get(event_id=event_id)
        except ObjectDoesNotExist as err:
            raise ValueError("Event not found.") from err

        expense_group_exists = EventExpenseGroup.objects.filter(
            event_participant__event=event_to_delete,
        ).exists()

        if expense_group_exists:
            raise ValueError("Cannot delete Event with associated EventExpenseGroup records.")

        return event_to_delete.delete()

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
    def delete_participant(
            self,
            participant_id: Optional[strawberry.ID] = None,
            participant_email: Optional[str] = None,
    ) -> bool:
        if not participant_id and not participant_email:
            raise ValueError("Either participant_id or participant_email must be provided.")

        participant_to_delete = None

        try:
            if participant_id:
                participant_to_delete = Participant.objects.get(participant_id=participant_id)
            elif participant_email:
                participant_to_delete = Participant.objects.get(participant_email=participant_email)
        except ObjectDoesNotExist as err:
            raise ValueError("Participant not found.") from err

        expense_group_exists = EventExpenseGroup.objects.filter(
            event_participant__participant=participant_to_delete,
        ).exists()

        if expense_group_exists:
            raise ValueError("Cannot delete Participant with associated EventExpenseGroup records.")

        return participant_to_delete.delete()

    @strawberry.mutation
    def add_participant_to_event(
            self,
            event_id: str,
            participant_id: str,
    ) -> EventParticipantType:

        if not Event.objects.filter(event_id=event_id).exists():
            raise ValueError(f"Event with ID {event_id} does not exist.")

        if not Participant.objects.filter(participant_id=participant_id).exists():
            raise ValueError(f"Participant with ID {participant_id} does not exist.")

        if EventParticipant.objects.filter(event__event_id=event_id,
                                           participant__participant_id=participant_id).exists():
            raise ValueError(
                f"EventParticipant record with Event ID {event_id} and Participant ID {participant_id} already exists.")

        event_to_add = Event.objects.get(event_id=event_id)
        participant_to_add = Participant.objects.get(participant_id=participant_id)
        new_event_participant = EventParticipant(event=event_to_add, participant=participant_to_add)
        new_event_participant.save()

        return EventParticipantType(
            event_participant_registered_at=new_event_participant.event_participant_registered_at,
            event_participant_id=new_event_participant.event_participant_id,
            participant=participant_to_add,
            event=event_to_add,
        )

    @strawberry.type
    class DeleteParticipantFromEventResult:
        success: bool
        deleted_event_participant: Optional[EventParticipantType] = None

    @strawberry.mutation
    def delete_participant_from_event(
            self,
            event_id: str,
            participant_id: str,
    # ) -> EventParticipantType:
    ) -> DeleteParticipantFromEventResult:

        try:
            event_participant = EventParticipant.objects.get(
                event__event_id=event_id,
                participant__participant_id=participant_id,
            )
        except ObjectDoesNotExist as err:
            raise ValueError(
                f"EventParticipant record with Event ID {event_id} and Participant ID {participant_id} does not exist.",
            ) from err

        return event_participant.delete()


schema = strawberry.Schema(query=Query, mutation=Mutation)
