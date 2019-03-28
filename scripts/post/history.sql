INSERT INTO history VALUES (
	0,
	%s,
	0,
	-- SELECT id FROM spool WHERE status_id = (SELECT id FROM status WHERE name = "Active"),
	%s,
	(SELECT status.id FROM status WHERE status.name = 'To Do'),
	%s,
	%s,
	%s,
	%s,
	(SELECT prints.id FROM prints WHERE prints.filename = %s)
)