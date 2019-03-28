INSERT INTO user VALUES(
    %s,
    %s,
    0,
    (SELECT status.id FROM status WHERE status.name = "Active" ),
    %s
)