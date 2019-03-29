SELECT p.id, p.filename, p.name, p.time, p.length, p.weight, p.price FROM prints p INNER JOIN history h ON
    p.id = h.printsId
    WHERE h.statusId = (SELECT s.id from status s WHERE s.name = "%s")