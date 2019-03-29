SELECT p.id, p.filename, p.name, p.time, p.length, p.weight, p.price, p.time_real FROM prints p INNER JOIN history h ON
    p.id = h.prints_id
    WHERE h.status = (SELECT status.id from status WHERE status.name = "%s")