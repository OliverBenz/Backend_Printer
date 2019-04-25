SELECT g.name from usergroup g INNER JOIN user u ON
    u.groupId = g.id WHERE u.sessionId = '%s';