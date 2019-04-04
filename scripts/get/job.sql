SELECT * FROM prints p INNER JOIN job j ON p.id = j.printsId
    WHERE j.userId = (SELECT u.id FROM user u WHERE u.sessionId = "%s")
    AND j.statusId = (SELECT s.id FROM status s WHERE s.name = "%s");