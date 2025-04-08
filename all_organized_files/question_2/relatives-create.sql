CREATE TABLE relatives (
    person_id INT  NOT NULL,
    relative_id INT NOT NULL,
    connection_id INT NOT NULL,
	PRIMARY KEY (person_id,relative_id,connection_id),
    FOREIGN KEY (connection_id) REFERENCES connection(connection_id)
);

drop table relatives

--FATHER
insert into relatives (person_id,relative_id,connection_id)
select person_id,father_id,1
FROM PERSON
WHERE father_id is not null

union
--MOTHER
--insert into relatives (person_id,relative_id,connection_id)
select person_id,mother_id,2
FROM PERSON
WHERE mother_id is not null

union
--BROTHER
--insert into relatives (person_id,relative_id,connection_id)
select P1.person_id,P2.person_id,3
FROM PERSON P1,PERSON P2
WHERE P1.person_id<>P2.person_id
	AND P2.gender='Male'
	AND (P1.father_id=P2.father_id OR P1.mother_id=P2.mother_id)

union
--SISTER
--insert into relatives (person_id,relative_id,connection_id)
select P1.person_id,P2.person_id,4
FROM PERSON P1,PERSON P2
WHERE P1.person_id<>P2.person_id
	AND P2.gender='Female'
	AND (P1.father_id=P2.father_id OR P1.mother_id=P2.mother_id)

union
--SON
select father_id,person_id,5
from person
where gender='Male'
and father_id is not NULL
union
select mother_id,person_id,5
from person
where gender='Male'
and mother_id is not NULL

union
--DAUGHTER
select father_id,person_id,6
from person
where gender='Female'
and father_id is not NULL
union
select mother_id,person_id,6
from person
where gender='Female'
and mother_id is not NULL

union
--HUSBAND AND COMPLETING DATA
select person_id,spouse_id,7
from person
where gender='Female'
and spouse_id is not NULL
union					--if she is updated as his wife, but he is not updated as her husband
select spouse_id,person_id,7
from person
where gender='Male'
and spouse_id is not NULL

union
--WIFE AND COMPLETING DATA
select person_id, spouse_id,8
from person
where gender='Male'
and spouse_id is not NULL
union					--if he is updated as her husband, but she is not updated as his wife
select spouse_id,person_id,8
from person
where gender='Female'
and spouse_id is not NULL


select * from relatives r join connection c 
on r.connection_id=c.connection_id




	
