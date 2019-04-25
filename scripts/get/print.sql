SELECT p.id, p.filename, p.name, p.time, p.length, p.weight FROM print p INNER JOIN job j ON
    p.id = j.printId
    WHERE j.statusId = (SELECT s.id from status s WHERE s.name = "%s");