UPDATE job j
    SET j.statusId = (SELECT s.id from status s WHERE s.name = '%s')
    WHERE j.id = '%s';