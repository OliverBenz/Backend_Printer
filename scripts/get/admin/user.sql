SELECT u.id, u.name, u.email, g.name as groupname FROM user u
	INNER JOIN usergroup g ON u.groupId = g.id
    	WHERE g.name = '%s'