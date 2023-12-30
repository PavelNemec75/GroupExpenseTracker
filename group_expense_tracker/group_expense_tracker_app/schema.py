from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union
import strawberry
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from graphql import GraphQLError
from strawberry import relay
from django.db.models import Count, F, OuterRef, Subquery, Window
from django.db.models.functions import RowNumber

from .types import ErrorResult, EventDataViewType, EventType, ParticipantType, SuccessResult
from .models import Event, EventExpenseGroup, EventExpenseItem, EventParticipant, Participant


# @strawberry.field
# def get_event_data_view(  # noqa: PLR0913
#         event_id: Optional[str] = None,
#         first: Optional[int] = None,
#         after: Optional[str] = None,
#         last: Optional[int] = None,
#         before: Optional[str] = None,
# ) -> EventDataViewConnection:
#     queryset = Event.objects
#
#     if event_id is not None:
#         queryset = queryset.filter(id=event_id)
#
#     subquery = (
#         EventExpenseGroup.objects
#         .filter(event_expense_item_id=OuterRef("item_id"))
#         .values("event_expense_item_id")
#         .annotate(count=Count("event_participant_id"))
#         .values("count")
#     )
#
#     queryset = (
#         queryset.annotate(
#             event_id=F("id"),
#             view_id=Window(
#                 expression=RowNumber(),
#                 order_by=(
#                     F("name").asc(),
#                     F("eventparticipant__eventexpensegroup__event_expense_item__name").asc(),
#                     F("eventparticipant__participant__first_name").asc(),
#                     F("eventparticipant__participant__last_name").asc(),
#                 ),
#             ) - 1,
#             event_name=F("name"),
#             item_name=F("eventparticipant__eventexpensegroup__event_expense_item__name"),
#             item_id=F("eventparticipant__eventexpensegroup__event_expense_item__id"),
#             participant_id=F("eventparticipant__participant_id"),
#             first_name=F("eventparticipant__participant__first_name"),
#             last_name=F("eventparticipant__participant__last_name"),
#             price=F("eventparticipant__eventexpensegroup__event_expense_item__price_eur"),
#             paid=F("eventparticipant__eventexpensegroup__paid_eur"),
#             balance=F("eventparticipant__eventexpensegroup__paid_eur") - F(
#                 "eventparticipant__eventexpensegroup__event_expense_item__price_eur") / Subquery(subquery)
#
#         ).order_by("event_name", "item_name", "first_name", "last_name")
#     )
#
#     total_count = len(queryset)
#     has_next_page = total_count / first > 0 if first is not None else False
#     has_previous_page = total_count / last > 0 if last is not None else False
#
#     def convert_queryset(queryset, custom_type, first, last):
#         data_list = queryset.values()
#
#         objects = [
#             custom_type(
#                 event_id=entry["event_id"],
#                 view_id=entry["view_id"],
#                 event_name=entry["event_name"],
#                 participant_id=entry["participant_id"],
#                 first_name=entry["first_name"],
#                 last_name=entry["last_name"],
#                 item_id=entry["item_id"],
#                 item_name=entry["item_name"],
#                 price=entry["price"],
#                 paid=entry["paid"],
#                 balance=entry["balance"]
#             )
#             for entry in data_list
#         ]
#
#         if first is not None:
#             objects = objects[:first]
#         elif last is not None:
#             objects = objects[-last:]
#
#         return objects
#
#     if after:
#         queryset = queryset.filter(view_id__gt=int(base64.b64decode(after).decode("utf-8").split(":")[-1]))
#     elif before:
#         queryset = queryset.filter(view_id__lt=int(base64.b64decode(before).decode("utf-8").split(":")[-1]))
#
#     event_data_list = convert_queryset(queryset, EventDataViewType, first, last)
#
#     edges = [EventDataViewEdge(
#         node=event,
#         cursor=base64.b64encode(f"arrayconnection:{str(event.view_id)}".encode()).decode()  # noqa: RUF010
#     )
#         for event in event_data_list]
#
#     start_cursor = (
#         str(edges[0].cursor)
#         if edges
#         else None
#     )
#     end_cursor = (
#         str(edges[-1].cursor)
#         if edges
#         else None
#     )
#
#     return EventDataViewConnection(
#         edges=edges,
#         page_info=relay.PageInfo(
#             start_cursor=start_cursor,
#             end_cursor=end_cursor,
#             has_previous_page=has_previous_page,
#             has_next_page=has_next_page,
#         ),
#         total_count=total_count,
#     )


@strawberry.input
class EventParticipantInput:
    event_participant_id: str
    paid_eur: float


@strawberry.input
class CreateEventExpenseGroupInput:
    event_expense_item_name: str
    event_expense_item_price_eur: float
    participants: List[EventParticipantInput]


@strawberry.type
class CreateEventExpenseGroupOutput:
    event_expense_group_id: str


@strawberry.type
class Query:
    node: relay.Node = relay.node()

    @relay.connection(strawberry.django.relay.ListConnectionWithTotalCount[EventType])
    def get_events(
            self,
            id: Optional[str] = None,
    ) -> List[EventType]:
        queryset = Event.objects.all() if id is None else Event.objects.filter(id=id)
        if not queryset.exists():
            raise GraphQLError(f"Event with ID {id} not found")
        return queryset

    @relay.connection(strawberry.django.relay.ListConnectionWithTotalCount[ParticipantType])
    def get_participants(
            self,
            id: Optional[str] = None,
    ) -> List[ParticipantType]:
        queryset = Participant.objects.all() if id is None else Participant.objects.filter(id=id)
        if not queryset.exists():
            raise GraphQLError(f"Participant with ID {id} not found")
        return queryset

    @relay.connection(strawberry.django.relay.ListConnectionWithTotalCount[EventDataViewType])
    def get_event_data_view(
            self,
            id: Optional[str] = None,
    ) -> List[EventDataViewType]:
        queryset = Event.objects

        if id is not None:
            queryset = queryset.filter(id=id)

        subquery = (
            EventExpenseGroup.objects
            .filter(event_expense_item_id=OuterRef("item_id"))
            .values("event_expense_item_id")
            .annotate(count=Count("event_participant_id"))
            .values("count")
        )

        queryset = (
            queryset.annotate(
                event_id=F("id"),
                view_id=Window(
                    expression=RowNumber(),
                    order_by=(
                        F("name").asc(),
                        F("eventparticipant__eventexpensegroup__event_expense_item__name").asc(),
                        F("eventparticipant__participant__first_name").asc(),
                        F("eventparticipant__participant__last_name").asc(),
                    ),
                ) - 1,
                event_name=F("name"),
                item_name=F("eventparticipant__eventexpensegroup__event_expense_item__name"),
                item_id=F("eventparticipant__eventexpensegroup__event_expense_item__id"),
                participant_id=F("eventparticipant__participant_id"),
                first_name=F("eventparticipant__participant__first_name"),
                last_name=F("eventparticipant__participant__last_name"),
                price=F("eventparticipant__eventexpensegroup__event_expense_item__price_eur"),
                paid=F("eventparticipant__eventexpensegroup__paid_eur"),
                balance=F("eventparticipant__eventexpensegroup__paid_eur") - F(
                    "eventparticipant__eventexpensegroup__event_expense_item__price_eur") / Subquery(subquery)

            ).order_by("event_name", "item_name", "first_name", "last_name")
        )
        if not queryset.exists():
            raise GraphQLError(f"Event with ID {id} not found")
        return queryset


@strawberry.type
class Mutation:
    # create_event_result: Union[SuccessResult, ErrorResult]

    @strawberry.mutation
    def create_event(
            self,
            name: str,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
    ) -> Union[SuccessResult, ErrorResult]:

        if not name or len(name.strip()) == 0:
            return ErrorResult(success=False, message="Name must not be empty.")

        existing_event = Event.objects.filter(name=name).first()
        if existing_event:
            return ErrorResult(success=False, message=f"Event with name '{name}' already exists.", id=existing_event.id)

        try:
            new_event = Event(
                name=name,
                start_date=start_date,
                end_date=end_date,
            )
            new_event.save()
        except Exception as e:
            return ErrorResult(success=False, message=f"Failed to create event. Error: {str(e)}")  # noqa: RUF010

        return SuccessResult(success=True, message="Event created successfully.", id=new_event.id)

    @strawberry.mutation
    def delete_event(
            self,
            id: int,
    ) -> Union[SuccessResult, ErrorResult]:
        try:
            event_to_delete = Event.objects.get(id=id)
        except ObjectDoesNotExist:
            return ErrorResult(success=False, message=f"Event with id '{id}' not found.", id=id)

        expense_group_exists = EventExpenseGroup.objects.filter(
            event_participant__event=event_to_delete,
        ).exists()

        if expense_group_exists:
            return ErrorResult(success=False, message="Cannot delete Event with associated EventExpenseGroup records",
                               id=id)

        try:
            event_to_delete.delete()
        except Exception as e:
            return ErrorResult(success=False, message=f"Cannot delete Event: {e}", id=id)

        return SuccessResult(success=True, message="Event deleted successfully.", id=id)

    @strawberry.mutation
    def create_participant(
            self,
            email: str,
            first_name: str,
            last_name: str,
    ) -> Union[SuccessResult, ErrorResult]:

        if not email or len(email.strip()) == 0:
            return ErrorResult(success=False, message="Email must not be empty.")

        if not first_name or len(first_name.strip()) == 0:
            return ErrorResult(success=False, message="First name must not be empty.")

        if not last_name or len(last_name.strip()) == 0:
            return ErrorResult(success=False, message="Last name must not be empty.")

        existing_participant = Participant.objects.filter(email=email).first()
        if existing_participant:
            return ErrorResult(success=False, message=f"Participant with email address '{email}' already exists.",
                               id=existing_participant.id)

        try:
            new_participant = Participant(
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            new_participant.save()
        except Exception as e:
            return ErrorResult(success=False, message=f"Cannot create participant: {e}")

        return SuccessResult(success=True, message="Participant created successfully.", id=new_participant.id)

    @strawberry.mutation
    def delete_participant(
            self,
            id: Optional[strawberry.ID] = None,
            email: Optional[str] = None,
    ) -> Union[SuccessResult, ErrorResult]:

        if not id and not email:
            return ErrorResult(success=False, message="Either participant_id or participant_email must be provided.")

        participant_to_delete = None

        try:
            if id:
                participant_to_delete = Participant.objects.get(id=id)
            elif email:
                participant_to_delete = Participant.objects.get(email=email)

        except ObjectDoesNotExist as err:
            return ErrorResult(success=False, message=f"Participant not found: {err}")

        expense_group_exists = EventExpenseGroup.objects.filter(
            event_participant__participant=participant_to_delete,
        ).exists()

        if expense_group_exists:
            return ErrorResult(success=False,
                               message="Cannot delete Participant with associated EventExpenseGroup records.")

        try:
            participant_to_delete.delete()
        except Exception as e:
            return ErrorResult(success=False, message=f"Cannot delete Participant: {e}", id=id)

        return SuccessResult(success=True, message="Participant deleted successfully.", id=id)

    @strawberry.mutation
    def add_participant_to_event(
            self,
            event_id: int,
            participant_id: int,
    ) -> Union[SuccessResult, ErrorResult]:

        if not Event.objects.filter(id=event_id).exists():
            return ErrorResult(success=False, message=f"Event with ID {event_id} does not exist.", id=event_id)

        if not Participant.objects.filter(id=participant_id).exists():
            return ErrorResult(success=False, message=f"Participant with ID {participant_id} does not exist.",
                               id=participant_id)

        if EventParticipant.objects.filter(event__id=event_id,
                                           participant__id=participant_id).exists():
            return ErrorResult(success=False, message=f"EventParticipant record with Event ID {event_id} and "
                                                      f"Participant ID {participant_id} already exists.")
        try:
            event_to_add = Event.objects.get(id=event_id)
            participant_to_add = Participant.objects.get(id=participant_id)
            new_event_participant = EventParticipant(event=event_to_add, participant=participant_to_add)
            new_event_participant.save()
        except Exception as e:
            return ErrorResult(success=False, message=f"Cannot add participant to event: {e}")

        return SuccessResult(success=True, message="Participant added to event successfully.",
                             id=new_event_participant.id)

    @strawberry.mutation
    def delete_participant_from_event(
            self,
            event_id: str,
            participant_id: str,
    ) -> Union[SuccessResult, ErrorResult]:

        try:
            event_participant = EventParticipant.objects.get(
                event__id=event_id,
                participant__id=participant_id,
            )
        except ObjectDoesNotExist:
            return ErrorResult(success=False, message=f"EventParticipant record with Event ID {event_id} and "
                                                      f"Participant ID {participant_id} doest not exists.")

        try:
            event_participant.delete()
        except Exception as e:
            return ErrorResult(success=False, message=f"Cannot delete participant from event: {e}")

        return SuccessResult(success=True, message="Participant deleted successfully from event.")

    @strawberry.mutation
    def create_event_expense_group(self, input: CreateEventExpenseGroupInput) -> Union[SuccessResult, ErrorResult]:

        """ get last created event """
        last_created_event_id = Event.objects.order_by("-created_at").first().id

        """ check if there is at least one event """
        if last_created_event_id is None:
            return ErrorResult(success=False,
                               message="No events found. Cannot create EventExpenseGroup without an event.")

        """ get list of event_participants from mutation query """
        event_participant_ids = [participant_input.event_participant_id for participant_input in input.participants]

        """ tries to get same event_participants from the table """
        existing_event_participants = EventParticipant.objects.filter(pk__in=event_participant_ids)

        """ checks if all received event_participants exists in table """
        if existing_event_participants.count() != len(event_participant_ids):
            return ErrorResult(success=False,
                               message="One or more event_participant_id do not exist. Data will not be saved.")

        """ checks if total sum of paid_eur per participant is equal to total_item price """
        total_paid_eur = sum(participant_input.paid_eur for participant_input in input.participants)
        if total_paid_eur != input.event_expense_item_price_eur:
            return ErrorResult(success=False,
                               message="The sum of paid_eur does not match event_expense_item_price_eur. "
                                       "Data will not be saved.")

        """ checks if event_expense_item_name is not empty or None, and event_expense_item_price_eur is not empty,
        None, and greater than zero """
        if (not input.event_expense_item_name or input.event_expense_item_price_eur is None or
                input.event_expense_item_price_eur <= 0):
            return ErrorResult(success=False,
                               message="Invalid input for event_expense_item_name or event_expense_item_price_eur. "
                                       "Data will not be saved.")

        try:
            with transaction.atomic():
                """ saves new event expense item """
                new_event_expense_item = EventExpenseItem.objects.create(  # noqa: F841
                    name=input.event_expense_item_name,
                    price_eur=input.event_expense_item_price_eur,
                )

                for participant_input in input.participants:
                    new_event_expense_group_record = EventExpenseGroup.objects.create(  # noqa: F841
                        paid_eur=participant_input.paid_eur,
                        event_expense_item_id=new_event_expense_item.id,
                        event_participant_id=participant_input.event_participant_id,
                    )

        except Exception as e:
            return ErrorResult(success=False, message=f"Cannot create new event expense group: {e}")

        return SuccessResult(success=True, message="Event expense group created successfully.")

    @strawberry.mutation
    def delete_expense_item(
            self,
            event_expense_item_id: int,
    ) -> Union[SuccessResult, ErrorResult]:

        """ check if event expense item exists """
        try:
            expense_item_to_delete = EventExpenseItem.objects.filter(id=event_expense_item_id)
            """ find if at least one record exits """
            if not expense_item_to_delete:
                return ErrorResult(success=False, message="Event expense item not found.")
        except Exception as e:
            return ErrorResult(success=False, message=f"Error finding event expense item: {e}")

        try:

            with transaction.atomic():
                expense_groups_to_delete = EventExpenseGroup.objects.filter(
                    event_expense_item_id=event_expense_item_id,
                )

                for expense_group_to_delete in expense_groups_to_delete:
                    expense_group_to_delete.delete()

                event_expense_item_to_delete = EventExpenseItem.objects.get(
                    id=event_expense_item_id
                )
                event_expense_item_to_delete.delete()

        except Exception as e:
            return ErrorResult(success=False, message=f"Cannot delete event expense item: {e}")

        return SuccessResult(success=True, message="Event expense item successfully deleted.")


schema = strawberry.Schema(query=Query, mutation=Mutation)

with Path("../schema.graphql").open("w") as file:
    file.write(schema.as_str())
