CREATE TABLE closest_subway_to_park AS
With circle AS (SELECT name AS subway_name,
                       subway_id,
                       ST_Transform(
                               ST_Buffer(
                                       ST_Transform(wkb_geometry, 3857),
                                       1000
                               ),
                               32634
                       )    AS circle_point
                FROM subway),

     park_and_point AS (SELECT wkb_geometry, point_park.point_id AS park_point_id, park_id
                        FROM point_park
                                 JOIN point_of_park ON point_park.point_id = point_of_park.point_id),
     park_and_subway AS (SELECT subway_name, park_id, subway_id, ST_Intersects(circle_point, wkb_geometry) AS is_in_circle
                         FROM circle,
                              park_and_point
                         WHERE ST_Intersects(circle_point, wkb_geometry) = true)

SELECT DISTINCT subway_id, park_id
FROM park_and_subway;
