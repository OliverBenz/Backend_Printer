INSERT INTO user VALUES(
    0,
    (SELECT ug.id from userGroup ug WHERE ug.name = "Registered"),
    %s,
    %s,
    %s,
    0.00,
    (SELECT s.id from status s WHERE s.name = "Active"),
    %s
);