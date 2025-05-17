CREATE TABLE district_of_park AS
    (With point_and_park AS (SELECT park_point.*, park_id
                              FROM park_point
                              JOIN point_of_park ON point_of_park.point_id = park_point.point_id)

                                  SELECT DISTINCT park_id, district_id
                                  FROM district,
                                       point_and_park
                                  WHERE ST_Intersects(point_and_park.wkb_geometry, district.wkb_geometry) = true)

