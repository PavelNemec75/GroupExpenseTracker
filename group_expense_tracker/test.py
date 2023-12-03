from pprint import pprint

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="http://127.0.0.1:8000/graphql")

client = Client(transport=transport, fetch_schema_from_transport=True)

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

result = client.execute(query)

pprint(result)
