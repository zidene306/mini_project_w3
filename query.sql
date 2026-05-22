select * from entity;

select * from year;

select * from indicator;

select * from fact_energy;

SELECT COUNT(*)
FROM fact_energy;

select y.year as year,
    i.indicator_name as indicator,
    value
from fact_energy f
join entity e
on f.entity_id=e.entity_id
join year y
on f.year_id=y.year_id
join indicator i
on f.indicator_id=i.indicator_id
where e.entity_name='Europe' and i.indicator_name='renewables_share_energy'
order by y.year;