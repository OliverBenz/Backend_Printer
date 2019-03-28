! add tables/columns lowercase

User
ID	Name		Balance		PrintCount

Finance example: at end of spool (id, 1, printCost, 23,22) 
Finance
ID	User_ID(FK)		Expsense		Amount	Date	Description


Spool
ID	Type		Brand		Colour		Price	Status_ID(FK)


Prints
ID	Filename	Name		Time	Length		Weight		Price		Time_real


History
ID	User_ID(FK)		Spool_ID(FK)	Amount	Status_id(FK)		Date		Date_till	Date_planned	Date_done	Prints_ID(FK)

Status
id	name


-- Insert new Queue
INSERT INTO prints VALUES(
	0,
	filenameVariable,
	nameVariable,
	timeVariable,
	lengthVariable,
	weightVariable,
	priceVariable,
	time_realVariable
)

INSERT INTO history VALUES (
	0,
	userIdVariable,
	0,
	-- SELECT TOP id FROM spool WHERE status_id = (SELECT id FROM status WHERE name = "Active"),
	amountVariable,
	SELECT id FROM status WHERE name = "To Do",
	dateVariable,
	date_tillVariable,
	date_plannedVariable,
	date_doneVariable,
	SELECT id FROM prints WHERE filename = filenameVariable
)