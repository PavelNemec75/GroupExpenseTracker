import sys
from pprint import pprint # noqa F401

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError # noqa F401
from graphql import GraphQLError

def test_exit():
    print("error")
    sys.exit()

transport = AIOHTTPTransport(url="http://127.0.0.1:8000/graphql")

client = Client(transport=transport, fetch_schema_from_transport=True)

# query = gql(
#     """
#     query GetEvents {
#       getEvents {
#         eventId
#         eventName
#       }
#     }
#     """,
# )
#
# result = client.execute(query)
# pprint(result)

query = gql(
    """
    query GetEvents {
      getEvents {
        eventId
        eventName
      }
    }
    """,
)


try:
    result = client.execute(query)
    test_exit()
except GraphQLError as e:
    print(f"expected error: {e}")
    assert isinstance(e, GraphQLError), f"Unexpected exception: {e}"  # noqa: S101

