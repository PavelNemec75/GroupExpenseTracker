import uuid
from datetime import datetime

import strawberry
from typing import List
from typing import Optional

from django.db import transaction

from .models import Event, Participant, EventParticipant, EventExpenseItem, EventExpenseGroup
from .types import EventType, ParticipantType, EventParticipantType, EventExpenseItemType, EventExpenseGroupType
from django.core.exceptions import ObjectDoesNotExist


@strawberry.input
class ParticipantInput:
    event_participant_id: str
    paid_eur: float


@strawberry.input
class CreateEventExpenseGroupInput:
    event_expense_item_name: str
    event_expense_item_price_eur: float
    participants: List[ParticipantInput]


@strawberry.type
class CreateEventExpenseGroupOutput:
    event_expense_group_id: str


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
            participant_first_name: str,
            participant_last_name: str,
    ) -> ParticipantType:
        existing_participant = Participant.objects.filter(participant_email=participant_email).first()
        if existing_participant:
            raise ValueError(f"Participant with email address \"{participant_email}\" already exists.")

        new_participant = Participant(
            participant_email=participant_email,
            participant_first_name=participant_first_name,
            participant_last_name=participant_last_name,
        )
        new_participant.save()

        return ParticipantType(
            participant_created_at=new_participant.participant_created_at,
            participant_email=new_participant.participant_email,
            participant_first_name=new_participant.participant_first_name,
            participant_last_name=new_participant.participant_last_name,
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

    @strawberry.mutation
    def delete_participant_from_event(
            self,
            event_id: str,
            participant_id: str,
    ) -> bool:

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

    @strawberry.mutation
    def create_event_expense_group(self, input: CreateEventExpenseGroupInput) -> CreateEventExpenseGroupOutput:

        """ get last created event """
        last_created_event = Event.objects.order_by('-event_created_at').first()

        if last_created_event is None:
            raise ValueError("No events found. Cannot create EventExpenseGroup without an event.")

        """ get list of event_participants from mutation query """
        event_participant_ids = [participant_input.event_participant_id for participant_input in input.participants]

        """ tries to get same event_participants from the table """
        existing_event_participants = EventParticipant.objects.filter(pk__in=event_participant_ids)

        """ checks if all received event_participants exists in table """
        if existing_event_participants.count() != len(event_participant_ids):
            raise ValueError("One or more event_participant_id do not exist. Data will not be saved.")

        """ checks if total sum of paid_eur per participant is equal to total_item price """
        total_paid_eur = sum(participant_input.paid_eur for participant_input in input.participants)
        if total_paid_eur != input.event_expense_item_price_eur:
            raise ValueError("The sum of paid_eur does not match event_expense_item_price_eur. Data will not be saved.")

        """ checks if event_expense_item_name is not empty or None, and event_expense_item_price_eur is not empty,
        None, and greater than zero """
        if (not input.event_expense_item_name or input.event_expense_item_price_eur is None or
                input.event_expense_item_price_eur <= 0):
            raise ValueError(
                "Invalid input for event_expense_item_name or event_expense_item_price_eur. Data will not be saved.")

        with transaction.atomic():

            """ saves new event expense item """
            new_event_expense_item_id = str(uuid.uuid4())
            event_expense_item = EventExpenseItem.objects.create(  # noqa: F841
                event_expense_item_id=new_event_expense_item_id,
                event_expense_item_name=input.event_expense_item_name,
                event_expense_item_price_eur=input.event_expense_item_price_eur,
            )

            event_expense_groups = []
            new_event_expense_group_id = str(uuid.uuid4())

            for participant_input in input.participants:
                # event_participant = EventParticipant.objects.get(pk=participant_input.event_participant_id)
                event_expense_group = EventExpenseGroup.objects.create(  # noqa: F841
                    event_expense_group_id=new_event_expense_group_id,
                    paid_eur=participant_input.paid_eur,
                    event_expense_item_id=new_event_expense_item_id,
                    event_participant_id=participant_input.event_participant_id,
                )
                event_expense_groups.append(event_expense_group)

        return CreateEventExpenseGroupOutput(event_expense_group_id=new_event_expense_group_id)

    @strawberry.mutation
    def delete_expense_group(
            self,
            event_expense_group_id: str,
    ) -> bool:

        """ check if event expense group exists """
        try:
            expense_group_to_delete = EventExpenseGroup.objects.filter(event_expense_group_id=event_expense_group_id)
            """ find if at least one record exits """
            if not expense_group_to_delete.exists():
                raise ValueError("Event expense group not found.")  # noqa: TRY301
        except Exception as err:
            raise ValueError("Event expense group not found.") from err

        event_expense_item_id_to_delete = next(
            iter(expense_group_to_delete.values_list("event_expense_item_id", flat=True)), None)

        event_expense_items_to_delete = EventExpenseItem.objects.filter(
            event_expense_item_id=event_expense_item_id_to_delete)

        with transaction.atomic():

            """ delete all records from event_expense_group table """
            for expense_group in expense_group_to_delete:
                expense_group.delete()

            """ delete all records from event_expense_item table """
            for event_expense_item in event_expense_items_to_delete:
                event_expense_item.delete()

        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
