-- The main information of park.
CREATE TABLE IF NOT EXISTS park
(
    park_id     INT primary key,
    park_name   text,
    attractions text,
    area        float,
    address     text,
    rating      float,
    district_id int not null,
    foreign key (district_id) REFERENCES district (district_id)
);

-- Districts of Warsaw.
CREATE TABLE IF NOT EXISTS district
(
    district_id INT primary key,
    name        text
);

-- District of park.
CREATE TABLE IF NOT EXISTS district_of_park
(
    district_id int,
    park_id     int,
    primary key (park_id, district_id),
    foreign key (district_id) REFERENCES district (district_id),
    foreign key (park_id) REFERENCES park (park_id)

);

CREATE TABLE IF NOT EXISTS street
(
    street_id   int primary key,
    street_name text
);

CREATE TABLE IF NOT EXISTS street_of_park
(
    street_id int,
    park_id   int,
    primary key (park_id, street_id),
    foreign key (street_id) REFERENCES street (street_id),
    foreign key (park_id) REFERENCES park (park_id)

);
