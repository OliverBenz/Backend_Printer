INSERT INTO history VALUES (
	0,
	%s,
	(SELECT s.id FROM spool s WHERE s.statusId = (SELECT st.id FROM status st WHERE st.name = 'Active')),
	%s,
	(SELECT s.id FROM status s WHERE s.name = 'To Do'),
	%s,
	%s,
	%s,
	%s
);