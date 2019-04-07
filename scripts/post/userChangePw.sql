UPDATE user u SET u.password = "%s", u.sessionId = "%s"
    WHERE sessionId = "%s";