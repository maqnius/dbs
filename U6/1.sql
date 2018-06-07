#1.1
insert into studierende (vorname, nachname, matrikelnummer) values
('Conrad', 'Hancke', 3197786),
('Herbert', 'Putzke', 5132147),
...
;

# Dozierende unterrichten
INSERT INTO unterrichtet(
            dozierender, lehrveranstaltung)
    VALUES (12378, 19202801),
    (18993, 19211601),
    (21435, 19215701),
    (22364, 19300313),
    (37152, 19302801),
    (11111, 19325911);

# Studenten hören
INSERT INTO hoert(
            studierender, lehrveranstaltung)
    VALUES 
    (3197786, 19202801),
    (4132587, 19211601),
    (5132147, 19215701),
    (5134789, 19300313),
    (5784348, 19302801),
    (3197786, 19325911),
    (4132587, 19202801),
    (5132147, 19211601),
    (5134789, 19215701),
    (5784348, 19300313);

# 1.2
select (matrikelnummer, nachname, vorname) from studierende order by nachname, vorname limit 5;

# 2.1
select count(lv_nummer) from lehrveranstaltungen where semester = 'SoSe 2018';


# 2.2
select doz.nachname, k.c from (
	select s.d as doz, count(s.l) as c from (
		select u.dozierender as d, u.lehrveranstaltung as l from 
		unterrichtet u 
		inner join  
		(
		   select matrikelnummer, lehrveranstaltung 
		   from studierende s inner join hoert h     
		   on s.matrikelnummer = h.studierender
		) x on (x.lehrveranstaltung = u.lehrveranstaltung)
		) s group by s.d ) k 
inner join dozierende doz on (doz.personalnummer = k.doz);

# 2.3
select sum(h.studierender) as s, l.name as lame
from hoert h
inner join lehrveranstaltungen l 
on (h.lehrveranstaltung = l.lv_nummer) group by l.name order by s desc limit 1;

# 3.1
