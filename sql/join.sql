





SELECT

    t1.event_id,
    t1.event_name,
    t1.event_start_date,
    t1.event_end_date,
    t1.event_created_at,
    
    t2.event_participant_id,
    t2.event_participant_registered_at,
    t2.event_id,
    t2.participant_id,
    
	t3.participant_id, 
	t3.participant_email, 
	t3.participant_first_name, 
	t3.participant_last_name, 
	t3.participant_created_at,

	t4.id, 
	t4.event_expense_group_id, 
	t4.paid_eur, 
	t4.event_expense_item_id, 
	t4.event_participant_id,
	
	t5.event_expense_item_id, 
	t5.event_expense_item_name, 
	t5.event_expense_item_price_eur
	

FROM group_expense_tracker_app_event t1
LEFT JOIN group_expense_tracker_app_eventparticipant t2 ON t1.event_id = t2.event_id
LEFT JOIN group_expense_tracker_app_participant t3 ON t2.participant_id = t3.participant_id
LEFT JOIN group_expense_tracker_app_eventexpensegroup t4 ON t2.event_participant_id = t4.event_participant_id
LEFT JOIN group_expense_tracker_app_eventexpenseitem t5 ON t4.event_expense_item_id = t5.event_expense_item_id

WHERE t1.event_id = '1ff70029-583d-4dc9-8bf6-279492a306a5';




