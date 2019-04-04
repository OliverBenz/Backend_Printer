SELECT p.id, p.filename, p.name, p.time, p.length, p.weight, p.price FROM prints p INNER JOIN job j ON
    p.id = j.printsId
    WHERE j.statusId = (SELECT s.id from status s WHERE s.name = "%s")