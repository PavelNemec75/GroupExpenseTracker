import strawberry
from strawberry import relay
from strawberry.types import Info

from . import models
from datetime import datetime
from typing import Iterable, List, Optional


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




# event_expense_item, event_expense_item_id, event_participant, event_participant_id, id, paid_eur",


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


# @strawberry.django.type(models.Event)
# class CustomType(relay.Node):
#     id: relay.NodeID[str]  # noqa: A003
#     event: EventType
#
#     # event_participant: EventParticipantType
#     # participant: ParticipantType
#
#     @strawberry.field
#     def custom_resolver(self) -> List:
#         all_fruits = {
#             1: {"code": 1, "name": "Jablko", "weight": 0.2},
#             2: {"code": 2, "name": "Banán", "weight": 0.3},
#             3: {"code": 3, "name": "Hruška", "weight": 0.25},
#             4: {"code": 4, "name": "Kiwi", "weight": 0.4},
#             5: {"code": 5, "name": "Pomeranč", "weight": 0.35},
#             6: {"code": 6, "name": "Malina", "weight": 0.1},
#             7: {"code": 7, "name": "Ananas", "weight": 0.5},
#             8: {"code": 8, "name": "Jahoda", "weight": 0.15},
#             9: {"code": 9, "name": "Hrozny", "weight": 0.6},
#             10: {"code": 10, "name": "Mango", "weight": 0.45},
#         }
#         all_fruits_list = list(all_fruits.values())
#         return all_fruits_list
# return models.Event.objects.filter(id=1)


# @strawberry.type
# class EventEdge:
#     node: EventType
#     cursor: str
#
#
# @strawberry.type
# class EventConnection(strawberry.django.type):
#     class Edges:
#         node: EventEdge
#     page_info: strawberry.django.type


@strawberry.type
class FruitType(relay.Node):
    id: relay.NodeID[str]  # noqa: A003
    name: str
    weight: float

    @staticmethod
    def from_id(id: relay.NodeID[str], info: Info) -> Optional['FruitType']:
        all_fruits = {
            1: {"code": 1, "name": "Jablko", "weight": 0.2},
            2: {"code": 2, "name": "Banán", "weight": 0.3},
            3: {"code": 3, "name": "Hruška", "weight": 0.25},
            4: {"code": 4, "name": "Kiwi", "weight": 0.4},
            5: {"code": 5, "name": "Pomeranč", "weight": 0.35},
            6: {"code": 6, "name": "Malina", "weight": 0.1},
            7: {"code": 7, "name": "Ananas", "weight": 0.5},
            8: {"code": 8, "name": "Jahoda", "weight": 0.15},
            9: {"code": 9, "name": "Hrozny", "weight": 0.6},
            10: {"code": 10, "name": "Mango", "weight": 0.45},
        }
        return all_fruits.get(int(id))

@strawberry.django.connection
class FruitConnection(FruitType):
    pass