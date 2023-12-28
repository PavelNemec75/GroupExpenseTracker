# from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List, Optional

import strawberry
from strawberry import relay
from strawberry.relay import Connection, Edge, PageInfo
from strawberry.types import Info

# from typing import List
# from typing import Optional

# from django.db import transaction

from .models import Event, Participant, EventParticipant, EventExpenseGroup, EventExpenseItem
from .types import (
    EventType, ParticipantType, EventParticipantType,  # , CustomType, EventConnection, EventEdge
    # , EventExpenseGroupType, EventExpenseItemType
)

# from django.core.exceptions import ObjectDoesNotExist


# @strawberry.input
# class EventParticipantInput:
#     event_participant_id: str
#     paid_eur: float
#
#
# @strawberry.input
# class CreateEventExpenseGroupInput:
#     event_expense_item_name: str
#     event_expense_item_price_eur: float
#     participants: List[EventParticipantInput]
#
#
# @strawberry.type
# class CreateEventExpenseGroupOutput:
#     event_expense_group_id: str


all_fruits = {
    1: {"id": 1, "name": "Jablko", "weight": 0.2},
    2: {"id": 2, "name": "Banán", "weight": 0.3},
    3: {"id": 3, "name": "Hruška", "weight": 0.25},
    4: {"id": 4, "name": "Kiwi", "weight": 0.4},
    5: {"id": 5, "name": "Pomeranč", "weight": 0.35},
    6: {"id": 6, "name": "Malina", "weight": 0.1},
    7: {"id": 7, "name": "Ananas", "weight": 0.5},
    8: {"id": 8, "name": "Jahoda", "weight": 0.15},
    9: {"id": 9, "name": "Hrozny", "weight": 0.6},
    10: {"id": 10, "name": "Mango", "weight": 0.45},
}


@strawberry.type
class FruitType(relay.Node):
    id: relay.NodeID[str]
    name: str
    weight: float

    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: Info,
        node_ids: Iterable[str],
        required: bool = False,
    ):
        return [
            cls(
                id=str(fruit["id"]),
                name=fruit["name"],
                weight=fruit["weight"]
            )
            for nid, fruit in all_fruits.items()
            if nid in node_ids
        ]


@strawberry.type
class FruitConnection:
    edges: List[FruitType]
    total_count: int
    page_info: relay.PageInfo

@strawberry.type
class Query:

    node: relay.Node = relay.node()

    # @relay.connection(relay.ListConnection[FruitType])
    # def fruits(self) -> Iterable[FruitType]:
    #     return [FruitType(id=str(fruit["id"]), name=fruit["name"], weight=fruit["weight"]) for fruit in all_fruits.values()]


    @strawberry.field
    def fruits(
        self,
        info: Info,
        first: int = None,
        last: int = None,
        after: str = None,
        before: str = None,
    ) -> FruitConnection:
        fruits = list(all_fruits.values())

        # Apply pagination
        if after:
            start_index = next((index for index, fruit in enumerate(fruits) if fruit["id"] == int(after)), None)
            fruits = fruits[start_index + 1:]
        if before:
            end_index = next((index for index, fruit in enumerate(fruits) if fruit["id"] == int(before)), None)
            fruits = fruits[:end_index]

        # Apply first and last
        if first is not None:
            fruits = fruits[:first]
        elif last is not None:
            fruits = fruits[-last:]

        page_info = relay.PageInfo(
            has_next_page=False,
            has_previous_page=False,
            start_cursor=str(fruits[0]["id"]) if fruits else None,
            end_cursor=str(fruits[-1]["id"]) if fruits else None,
        )

        return FruitConnection(edges=[FruitType(**fruit) for fruit in fruits], total_count=len(fruits), page_info=page_info)












    get_events: strawberry.django.relay.ListConnectionWithTotalCount[EventType] = (
        strawberry.django.connection())

    get_participants: strawberry.django.relay.ListConnectionWithTotalCount[ParticipantType] = (
        strawberry.django.connection())

    # get_custom: strawberry.django.relay.ListConnectionWithTotalCount[CustomType] = (
    #     strawberry.django.connection())
    #
    # fruits2: strawberry.django.relay.ListConnectionWithTotalCount[FruitType] = (
    #     strawberry.django.connection())

    # from strawberry.django import auto
    #
    #
    # @strawberry.field
    # def get_events2(
    #         self,
    #         info,
    #         event_id: strawberry.ID,
    #         first: int = 10,
    #         after: str = None
    # ) -> EventConnection:
    #     queryset = EventParticipant.objects.filter(event_id=event_id)
    #
    #     if after:
    #         queryset = queryset.filter(id__gt=after)
    #
    #     event_participants = queryset[:first]
    #
    #     edges = [EventEdge(node=ep, cursor=str(ep.id)) for ep in event_participants]
    #
    #     return EventConnection(edges=edges, pageInfo=strawberry.types.PageInfo(
    #         hasNextPage=len(event_participants) > 0,
    #         endCursor=str(event_participants[-1].id) if event_participants else None))

    # @strawberry.field
    # def combined_data(self) -> List[EventParticipantType]:
    #     event_id = 1
    #     return EventParticipant.objects.filter(event_id=event_id) #.prefetch_related("eventexpensegroup_set")
    #     # return EventParticipant.objects.filter(event_id=event_id).prefetch_related("eventexpensegroup__event_expense_item__eventexpensegroup_set")
    #     # return EventParticipant.objects.filter(event_id=event_id).select_related("event", "participant").filter("eventexpensegroup__event_participant_set") #.eventexpensegroup_set.all() #.prefetch_related("eventexpensegroup_set__event_expense_item")
    #     # return Event.objects.prefetch_related('event_participants__eventexpensegroup_set')
    #
    # @strawberry.field
    # def event_with_participants(self, info, id: int) -> JoinedTypes:
    #
    #     event_data = Event.objects.filter(id=id).first()
    #     event_participant_data = EventParticipant.objects.select_related("event")
    #     participant_data = Participant.objects.prefetch_related("participant_events")
    #
    #     return JoinedTypes(
    #         event=event_data,
    #         event_participant=list(event_participant_data),
    #         participant=list(participant_data),
    #     )

    # Check results
    # if event is not None:
    #     # Convert event to GraphQL type
    #     event_type = EventType(
    #         id=relay.NodeID(),
    #         name=event.name,
    #         # participants=[EventParticipantType(
    #         #     id=relay.NodeID(),
    #         #     event=EventType(
    #         #         id=relay.NodeID(),
    #         #         name=ep.event.name,
    #         #         start_date=ep.event.start_date,
    #         #         end_date=ep.event.end_date,
    #         #         created_at=ep.event.created_at
    #         #     ),
    #         #     participant=ep.participant,  # you should convert participant to ParticipantType
    #         #     registered_at=ep.registered_at
    #         # ) for ep in event.eventparticipant_set.all()]
    #     )
    #     return event_type
    # return None

    # @strawberry.django.field
    # def get_events(self, info) -> List[EventType]:
    #     return Event.objects.prefetch_related('eventparticipant_set').all()
    #
    # get_events_paginated: List[EventType] = strawberry.django.relay.connection.field(get_events)

    # @strawberry.django.field
    # def get_events(self, info) -> strawberry.django.relay.ListConnectionWithTotalCount[EventType]:
    #     return Event.objects.prefetch_related('eventparticipant_set').all()
    #

    # @strawberry.django.field
    # def get_events(self, info) -> List[EventType]:
    #     queryset = Event.objects.select_related('eventparticipant_set').filter(eventparticipant_set=)
    #     return queryset
    # return strawberry.django.connection(queryset)

    # get_participants: strawberry.django.relay.ListConnectionWithTotalCount[ParticipantType] = (
    #     strawberry.django.connection())
    #
    # get_event_participants: strawberry.django.relay.ListConnectionWithTotalCount[EventParticipantType] = (
    #     strawberry.django.connection())

    # def resolve_participants(root: ParticipantType, info) -> Iterable[ParticipantType]:
    #     return Participant.objects.select_related().filter(eventparticipant)
    #
    # def resolve_events(root, info) -> Iterable[EventType]:
    #     return Event.objects.prefetch_related('eventparticipant_set__participant').filter(event=root)

    # events: List[EventType] = strawberry.field(resolve_events)
    #
    # participants: List[ParticipantType] = strawberry.field(resolve_participants)

    # @strawberry.field
    # def get_events(self, info: Info) -> strawberry.types.ExecuteInfo:
    #     return mutations.get_list(EventType, Event.objects.all(), info)
    #
    # @strawberry.field
    # def get_participants(self, info: Info) -> strawberry.types.ExecuteInfo:
    #     return mutations.get_list(ParticipantType, Participant.objects.all(), info)
    #
    # @strawberry.field
    # def get_all_event_participants(self, info: Info) -> strawberry.types.ExecuteInfo:
    #     return mutations.get_list(
    #         EventParticipantType,
    #         EventParticipant.objects.select_related('participant', 'event').all(),
    #         info
    #     )

    #
    # @strawberry.field
    # def get_events(self) -> List[EventType]:
    #     return list(Event.objects.all())
    #
    # @strawberry.field
    # def get_participants(self) -> List[ParticipantType]:
    #     return list(Participant.objects.all())
    #
    # @strawberry.field
    # def get_all_event_participants(self) -> List[EventParticipantType]:
    #     return EventParticipant.objects.select_related('participant', 'event').all()
    #
    #
    #
    #
    #
    #
    #
    # @strawberry.field
    # def get_event_participants(
    #         self,
    #         event_id: str,
    # ) -> List[EventParticipantType]:
    #     try:
    #         event = Event.objects.get(event_id=event_id)
    #     except ObjectDoesNotExist as err:
    #         raise ValueError(f"Event with ID {event_id} does not exist.") from err
    #
    #     participants = EventParticipant.objects.filter(event=event)
    #     return [EventParticipantType(
    #         # event_id=participant.event_id,
    #         # participant_id=participant.participant_id,
    #         event_participant_id=participant.event_participant_id,
    #         event=participant.event,
    #         participant=participant.participant,
    #         event_participant_registered_at=participant.event_participant_registered_at,
    #
    #     ) for participant in participants]
    #
    # @strawberry.field
    # def get_event_expense_items(self) -> List[EventExpenseItemType]:
    #     return list(EventExpenseItem.objects.all())
    #
    # @strawberry.field
    # def get_event_expense_groups(self) -> List[EventExpenseGroupType]:
    #     return list(EventExpenseGroup.objects.all())


# @strawberry.type
# class Mutation:
#
#     @strawberry.mutation
#     def create_event(
#             self,
#             event_name: str,
#             event_start_date: Optional[datetime] = None,
#             event_end_date: Optional[datetime] = None,
#     ) -> EventType:
#         existing_event = Event.objects.filter(event_name=event_name).first()
#         if existing_event:
#             raise ValueError(f"Event with name \"{event_name}\"already exists.")
#
#         new_event = Event(
#             event_name=event_name,
#             event_start_date=event_start_date,
#             event_end_date=event_end_date,
#         )
#         new_event.save()
#
#         return EventType(
#             event_id=new_event.event_id,
#             event_name=new_event.event_name,
#             event_start_date=new_event.event_start_date,
#             event_end_date=new_event.event_end_date,
#             event_created_at=new_event.event_created_at,
#         )
#
#     @strawberry.mutation
#     def delete_event(
#             self,
#             event_id: strawberry.ID,
#     ) -> bool:
#         try:
#             event_to_delete = Event.objects.get(event_id=event_id)
#         except ObjectDoesNotExist as err:
#             raise ValueError("Event not found.") from err
#
#         expense_group_exists = EventExpenseGroup.objects.filter(
#             event_participant__event=event_to_delete,
#         ).exists()
#
#         if expense_group_exists:
#             raise ValueError("Cannot delete Event with associated EventExpenseGroup records.")
#
#         return event_to_delete.delete()
#
#     @strawberry.mutation
#     def create_participant(
#             self,
#             participant_email: str,
#             participant_first_name: str,
#             participant_last_name: str,
#     ) -> ParticipantType:
#         existing_participant = Participant.objects.filter(participant_email=participant_email).first()
#         if existing_participant:
#             raise ValueError(f"Participant with email address \"{participant_email}\" already exists.")
#
#         new_participant = Participant(
#             participant_email=participant_email,
#             participant_first_name=participant_first_name,
#             participant_last_name=participant_last_name,
#         )
#         new_participant.save()
#
#         return ParticipantType(
#             participant_created_at=new_participant.participant_created_at,
#             participant_email=new_participant.participant_email,
#             participant_first_name=new_participant.participant_first_name,
#             participant_last_name=new_participant.participant_last_name,
#             participant_id=new_participant.participant_id,
#         )
#
#     @strawberry.mutation
#     def delete_participant(
#             self,
#             participant_id: Optional[strawberry.ID] = None,
#             participant_email: Optional[str] = None,
#     ) -> bool:
#         if not participant_id and not participant_email:
#             raise ValueError("Either participant_id or participant_email must be provided.")
#
#         participant_to_delete = None
#
#         try:
#             if participant_id:
#                 participant_to_delete = Participant.objects.get(participant_id=participant_id)
#             elif participant_email:
#                 participant_to_delete = Participant.objects.get(participant_email=participant_email)
#         except ObjectDoesNotExist as err:
#             raise ValueError("Participant not found.") from err
#
#         expense_group_exists = EventExpenseGroup.objects.filter(
#             event_participant__participant=participant_to_delete,
#         ).exists()
#
#         if expense_group_exists:
#             raise ValueError("Cannot delete Participant with associated EventExpenseGroup records.")
#
#         return participant_to_delete.delete()
#
#     @strawberry.mutation
#     def add_participant_to_event(
#             self,
#             event_id: str,
#             participant_id: str,
#     ) -> EventParticipantType:
#
#         if not Event.objects.filter(event_id=event_id).exists():
#             raise ValueError(f"Event with ID {event_id} does not exist.")
#
#         if not Participant.objects.filter(participant_id=participant_id).exists():
#             raise ValueError(f"Participant with ID {participant_id} does not exist.")
#
#         if EventParticipant.objects.filter(event__event_id=event_id,
#                                            participant__participant_id=participant_id).exists():
#             raise ValueError(
#                 f"EventParticipant record with Event ID {event_id} and "
#                 f"Participant ID {participant_id} already exists.")
#
#         event_to_add = Event.objects.get(event_id=event_id)
#         participant_to_add = Participant.objects.get(participant_id=participant_id)
#         new_event_participant = EventParticipant(event=event_to_add, participant=participant_to_add)
#         new_event_participant.save()
#
#         return EventParticipantType(
#             event_participant_registered_at=new_event_participant.event_participant_registered_at,
#             event_participant_id=new_event_participant.event_participant_id,
#             participant=participant_to_add,
#             event=event_to_add,
#         )
#
#     @strawberry.mutation
#     def delete_participant_from_event(
#             self,
#             event_id: str,
#             participant_id: str,
#     ) -> bool:
#
#         try:
#             event_participant = EventParticipant.objects.get(
#                 event__event_id=event_id,
#                 participant__participant_id=participant_id,
#             )
#         except ObjectDoesNotExist as err:
#             raise ValueError(
#                 f"EventParticipant record with Event ID {event_id} and "
#                 f"Participant ID {participant_id} does not exist.",
#             ) from err
#
#         return event_participant.delete()
#
#     @strawberry.mutation
#     def create_event_expense_group(self, input: CreateEventExpenseGroupInput) -> CreateEventExpenseGroupOutput:
#
#         """ get last created event """
#         last_created_event_id = Event.objects.order_by('-event_created_at').first().event_id
#
#         """ check if there is at least one event """
#         if last_created_event_id is None:
#             raise ValueError("No events found. Cannot create EventExpenseGroup without an event.")
#
#         """ get list of event_participants from mutation query """
#         event_participant_ids = [participant_input.event_participant_id for participant_input in input.participants]
#
#         """ tries to get same event_participants from the table """
#         existing_event_participants = EventParticipant.objects.filter(pk__in=event_participant_ids)
#
#         """ checks if all received event_participants exists in table """
#         if existing_event_participants.count() != len(event_participant_ids):
#             raise ValueError("One or more event_participant_id do not exist. Data will not be saved.")
#
#         """ checks if total sum of paid_eur per participant is equal to total_item price """
#         total_paid_eur = sum(participant_input.paid_eur for participant_input in input.participants)
#         if total_paid_eur != input.event_expense_item_price_eur:
#             raise ValueError("The sum of paid_eur does not match event_expense_item_price_eur. "
#                              "Data will not be saved.")
#
#         """ checks if event_expense_item_name is not empty or None, and event_expense_item_price_eur is not empty,
#         None, and greater than zero """
#         if (not input.event_expense_item_name or input.event_expense_item_price_eur is None or
#                 input.event_expense_item_price_eur <= 0):
#             raise ValueError(
#                 "Invalid input for event_expense_item_name or event_expense_item_price_eur. Data will not be saved.")
#
#         with transaction.atomic():
#
#             """ saves new event expense item """
#             new_event_expense_item_id = str(uuid.uuid4())
#             event_expense_item = EventExpenseItem.objects.create(  # noqa: F841
#                 event_expense_item_id=new_event_expense_item_id,
#                 event_expense_item_name=input.event_expense_item_name,
#                 event_expense_item_price_eur=input.event_expense_item_price_eur,
#             )
#
#             event_expense_groups = []
#             new_event_expense_group_id = str(uuid.uuid4())
#
#             for participant_input in input.participants:
#                 event_expense_group = EventExpenseGroup.objects.create(  # noqa: F841
#                     event_expense_group_id=new_event_expense_group_id,
#                     paid_eur=participant_input.paid_eur,
#                     event_expense_item_id=new_event_expense_item_id,
#                     event_participant_id=participant_input.event_participant_id,
#                 )
#                 event_expense_groups.append(event_expense_group)
#
#         return CreateEventExpenseGroupOutput(event_expense_group_id=new_event_expense_group_id)
#
#     @strawberry.mutation
#     def delete_expense_group(
#             self,
#             event_expense_group_id: str,
#     ) -> bool:
#
#         """ check if event expense group exists """
#         try:
#             expense_group_to_delete = EventExpenseGroup.objects.filter(event_expense_group_id=event_expense_group_id)
#             """ find if at least one record exits """
#             if not expense_group_to_delete.exists():
#                 raise ValueError("Event expense group not found.")  # noqa: TRY301
#         except Exception as err:
#             raise ValueError("Event expense group not found.") from err
#
#         event_expense_item_id_to_delete = next(
#             iter(expense_group_to_delete.values_list("event_expense_item_id", flat=True)), None)
#
#         event_expense_items_to_delete = EventExpenseItem.objects.filter(
#             event_expense_item_id=event_expense_item_id_to_delete)
#
#         with transaction.atomic():
#
#             """ delete all records from event_expense_group table """
#             for expense_group in expense_group_to_delete:
#                 expense_group.delete()
#
#             """ delete all records from event_expense_item table """
#             for event_expense_item in event_expense_items_to_delete:
#                 event_expense_item.delete()
#
#         return True


schema = strawberry.Schema(query=Query)
# schema = strawberry.Schema(query=Query, mutation=Mutation)

with Path("../schema.graphql").open("w") as file:
    file.write(schema.as_str())
