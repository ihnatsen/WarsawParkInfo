SELECT 
    name, subway_id,
    ST_Transform(
        ST_Buffer(
            ST_Transform(wkb_geometry, 3857),
            2000
        ),
        4326
    ) AS circle
FROM subway