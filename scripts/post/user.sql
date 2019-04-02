INSERT INTO user VALUES(
    0,
    %s,
    %s,
    %s,
    0.00,
    (SELECT s.id from status s WHERE s.name = "Active"),
    %s
)