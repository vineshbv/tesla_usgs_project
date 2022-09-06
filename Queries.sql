--Please query all events that have occurred during year 2017
Select count(Event_ID) as [Total Event of 2017] from Valuation.EventsOverview;

--Biggest EarthQuake of 2017
Select * from Valuation.EventsOverview
where Magnitude = (select max(Magnitude) from Valuation.EventsOverview)
and Type = 'earthquake';

--Probable Hour of the day per magnitude range
Select count(Event_ID) as NoOfEvents, [Hour], Magnitude_Range from Valuation.EventsOverview
where Type = 'earthquake'
group by [Hour], Magnitude_Range
order by [Hour], Magnitude_Range;
