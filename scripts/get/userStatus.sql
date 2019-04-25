SELECT s.name from status s INNER JOIN user u ON
    u.statusId = s.id WHERE u.sessionId = '%s';