-- DB schema for Events Table
CREATE TABLE Valuation.EventsOverview (
    Event_ID nvarchar(4000),
    [Type] nvarchar(4000),
    Title nvarchar(4000),
    [Date] nvarchar(4000),
	[Hour] nvarchar(4000),
    Magnitude float,
    Magnitude_Type nvarchar(4000),
    Magnitude_Range nvarchar(4000)
);