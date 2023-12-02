

delete from events;
delete from participants;
delete from event_participants;
delete from event_expense;
delete from event_expense_items;


-- events
INSERT INTO events (event_id, event_name, event_start_date, event_end_date, event_created_at) VALUES ('event_id_1', 'event_name_1', 1691184000, 1691270400, 1693601600);
INSERT INTO events (event_id, event_name, event_start_date, event_end_date, event_created_at) VALUES ('event_id_2', 'event_name_2', 1691184000, 1691270400, 1693601600);
INSERT INTO events (event_id, event_name, event_start_date, event_end_date, event_created_at) VALUES ('event_id_3', 'event_name_3', 1691184000, 1691270400, 1693601600);


-- participants
INSERT INTO participants (participant_id, participant_email, participant_created_at) VALUES ('participant_id_1', 'participant1@example.com', 1640979200);
INSERT INTO participants (participant_id, participant_email, participant_created_at) VALUES ('participant_id_2', 'participant2@example.com', 1640979200);
INSERT INTO participants (participant_id, participant_email, participant_created_at) VALUES ('participant_id_3', 'participant3@example.com', 1640979200);


-- event_participants
INSERT INTO event_participants (event_participant_id, participant_id, event_id, event_participant_registered_at) VALUES ('event_participant_id_1', 'participant_id_1', 'event_id_1', 1640979200);
INSERT INTO event_participants (event_participant_id, participant_id, event_id, event_participant_registered_at) VALUES ('event_participant_id_2', 'participant_id_2', 'event_id_1', 1640979200);
INSERT INTO event_participants (event_participant_id, participant_id, event_id, event_participant_registered_at) VALUES ('event_participant_id_3', 'participant_id_3', 'event_id_1', 1640979200);

INSERT INTO event_participants (event_participant_id, participant_id, event_id, event_participant_registered_at) VALUES ('event_participant_id_4', 'participant_id_1', 'event_id_2', 1640979200);
INSERT INTO event_participants (event_participant_id, participant_id, event_id, event_participant_registered_at) VALUES ('event_participant_id_5', 'participant_id_2', 'event_id_2', 1640979200);




-- event_expense
INSERT INTO event_expense (event_expense_id, event_expense_name, event_participant_id, event_expense_item_id) VALUES ('expense_id_1', 'event_expense_name_1', 'event_participant_id_1', 'expense_item_id_1');
INSERT INTO event_expense (event_expense_id, event_expense_name, event_participant_id, event_expense_item_id) VALUES ('expense_id_1', 'event_expense_name_1', 'event_participant_id_1', 'expense_item_id_1');
INSERT INTO event_expense (event_expense_id, event_expense_name, event_participant_id, event_expense_item_id) VALUES ('expense_id_1', 'event_expense_name_1', 'event_participant_id_1', 'expense_item_id_1');

INSERT INTO event_expense (event_expense_id, event_expense_name, event_participant_id, event_expense_item_id) VALUES ('expense_id_2', 'event_expense_name_2', 'event_participant_id_1', 'expense_item_id_1');
INSERT INTO event_expense (event_expense_id, event_expense_name, event_participant_id, event_expense_item_id) VALUES ('expense_id_3', 'event_expense_name_3', 'event_participant_id_1', 'expense_item_id_1');




-- event_expense_items 
INSERT INTO event_expense_items (event_expense_item_id, event_expense_item_name, event_expense_item_price_eur) VALUES ('expense_item_id_1', 'event_expense_item_name_1', 25.50);
INSERT INTO event_expense_items (event_expense_item_id, event_expense_item_name, event_expense_item_price_eur) VALUES ('expense_item_id_2', 'event_expense_item_name_2', 25.50);
INSERT INTO event_expense_items (event_expense_item_id, event_expense_item_name, event_expense_item_price_eur) VALUES ('expense_item_id_3', 'event_expense_item_name_3', 25.50);


