INSERT INTO job VALUES (
	0,
	(SELECT user.id FROM user WHERE user.sessionId = %s),
	(SELECT s.id FROM spool s WHERE s.statusId = (SELECT st.id FROM status st WHERE st.name = 'Active')),
	%s,
	(SELECT s.id FROM status s WHERE s.name = 'To Do'),
	%s,
	%s,
	%s,
	%s,
	%s
);