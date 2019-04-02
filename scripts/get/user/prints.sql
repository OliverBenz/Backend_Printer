SELECT * FROM prints p INNER JOIN history h ON p.id = h.printsId
    WHERE h.userId = (SELECT u.id FROM user u WHERE u.sessionId = "%s")
    AND h.statusId = (SELECT s.id FROM status s WHERE s.name = "%s");