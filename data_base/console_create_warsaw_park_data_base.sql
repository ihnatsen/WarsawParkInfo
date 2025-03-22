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
    foreign key (district_id) REFERENCES district(district_id)
);

-- Districts of Warsaw.
CREATE TABLE IF NOT EXISTS district
(
    district_id INT primary key,
    name        text
);
