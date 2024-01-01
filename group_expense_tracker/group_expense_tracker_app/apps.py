from django.apps import AppConfig
from django.db import connection


class GroupExpenseTrackerAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "group_expense_tracker_app"

    def ready(self):
        self.create_custom_view()

    def create_custom_view(self):
        view_query1 = "DROP VIEW IF EXISTS get_event_data_view2;"
        view_query2 = """
        CREATE VIEW get_event_data_view2 AS
        SELECT 
        (ROW_NUMBER() OVER (ORDER BY "group_expense_tracker_app_event"."name" ASC, "group_expense_tracker_app_eventexpenseitem"."name" ASC, "group_expense_tracker_app_participant"."first_name" ASC, "group_expense_tracker_app_participant"."last_name" ASC) - 1) AS "id", 
        "group_expense_tracker_app_event"."id" AS "event_id", 
        "group_expense_tracker_app_event"."name", 
        "group_expense_tracker_app_event"."start_date", 
        "group_expense_tracker_app_event"."end_date", 
        "group_expense_tracker_app_event"."created_at", 
        "group_expense_tracker_app_event"."name" AS "event_name", 
        "group_expense_tracker_app_eventexpenseitem"."name" AS "item_name", 
        "group_expense_tracker_app_eventexpensegroup"."event_expense_item_id" AS "item_id", 
        "group_expense_tracker_app_eventparticipant"."participant_id" AS "participant_id", 
        "group_expense_tracker_app_participant"."first_name" AS "first_name", 
        "group_expense_tracker_app_participant"."last_name" AS "last_name", 
        "group_expense_tracker_app_eventexpenseitem"."price_eur" AS "price", 
        "group_expense_tracker_app_eventexpensegroup"."paid_eur" AS "paid", 
        CAST(("group_expense_tracker_app_eventexpensegroup"."paid_eur" - CAST(("group_expense_tracker_app_eventexpenseitem"."price_eur" / (SELECT COUNT(U0."event_participant_id") AS "count" 
        FROM "group_expense_tracker_app_eventexpensegroup" U0 WHERE U0."event_expense_item_id" = ("group_expense_tracker_app_eventexpensegroup"."event_expense_item_id") GROUP BY U0."event_expense_item_id")) AS NUMERIC)) AS NUMERIC) AS "balance" FROM "group_expense_tracker_app_event" 
        LEFT OUTER JOIN "group_expense_tracker_app_eventparticipant" ON ("group_expense_tracker_app_event"."id" = "group_expense_tracker_app_eventparticipant"."event_id") 
        LEFT OUTER JOIN "group_expense_tracker_app_eventexpensegroup" ON ("group_expense_tracker_app_eventparticipant"."id" = "group_expense_tracker_app_eventexpensegroup"."event_participant_id") 
        LEFT OUTER JOIN "group_expense_tracker_app_eventexpenseitem" ON ("group_expense_tracker_app_eventexpensegroup"."event_expense_item_id" = "group_expense_tracker_app_eventexpenseitem"."id") 
        LEFT OUTER JOIN "group_expense_tracker_app_participant" ON ("group_expense_tracker_app_eventparticipant"."participant_id" = "group_expense_tracker_app_participant"."id") 
        ORDER BY 8 ASC, 9 ASC, 12 ASC, 13 ASC;
        """
        with connection.cursor() as cursor:
            cursor.execute(view_query1)
            cursor.execute(view_query2)

