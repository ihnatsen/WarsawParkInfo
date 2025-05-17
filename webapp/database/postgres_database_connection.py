from typing import List

import psycopg2
from psycopg2 import sql
from .database_interfaces import DatabaseInterface, Park


class PostgresDatabaseConnection(DatabaseInterface):
    __SQL_REQWEST_THE_TABLE = sql.SQL("""
    WITH percentiles AS (  
        SELECT
            percentile_disc(0.25) WITHIN GROUP (ORDER BY rating) AS p25,
            percentile_disc(0.50) WITHIN GROUP (ORDER BY rating) AS p50,
            percentile_disc(0.90) WITHIN GROUP (ORDER BY rating) AS p90
        FROM park
        
    ),
    park_category AS (SELECT park.*,
        CASE 
            WHEN rating < p25 THEN 'D'
            WHEN rating < p50 THEN 'C'
            WHEN rating < p90 THEN 'B'
            ELSE 'A'
        END AS rating_category
    FROM park, percentiles),
    
    subway_name_AND_clst_sbw_to_park AS (
        SELECT subway.name, closest_subway_to_park.park_id
        FROM subway JOIN closest_subway_to_park ON subway.subway_id = closest_subway_to_park.subway_id
    ),
    distrcit_name_AND_district_of_park AS(
        SELECT district.name, district_of_park.park_id
        FROM district JOIN district_of_park ON district.district_id = district_of_park.district_id
    ),
    park_category_AND_category_AND_district AS (
        SELECT
            park_category.name AS park_name,
            distrcit_name_AND_district_of_park.name AS distrcit_name,
            subway_name_AND_clst_sbw_to_park.name AS subway_name,
            park_category.attractions,
            park_category.area,
            park_category.rating,
            rating_category
        FROM park_category
            JOIN distrcit_name_AND_district_of_park
                ON park_category.park_id = distrcit_name_AND_district_of_park.park_id
            JOIN subway_name_AND_clst_sbw_to_park
                ON park_category.park_id = subway_name_AND_clst_sbw_to_park.park_id
    ),
    distrcit_names_list AS(
    SELECT
        park_name,
        string_agg(DISTINCT distrcit_name, ', ' ORDER BY distrcit_name) AS distrcit_names
    FROM park_category_AND_category_AND_district
    GROUP BY park_name),
    
    subway_names_list AS(
    SELECT
    park_name,
    string_agg(DISTINCT subway_name, ', ' ORDER BY subway_name) AS subway_names
    FROM park_category_AND_category_AND_district
    GROUP BY park_name),
    
    uniq_park AS (
        SELECT DISTINCT park_name AS name,
            attractions,
            area,
            rating,
            rating_category
        FROM park_category_AND_category_AND_district
    ),
    the_table AS (
    SELECT uniq_park.*,
           distrcit_names as districts,
           subway_names as subways
    FROM uniq_park
        JOIN distrcit_names_list ON distrcit_names_list.park_name = uniq_park.name
    JOIN  subway_names_list On subway_names_list.park_name = uniq_park.name)
    SELECT * from the_table
    """)

    __SQL_REQWEST_PARK_NAME = sql.SQL("""
    SELECT name FROM park
    """)

    def __init__(self, dbname, user, password, host, port):
        super().__init__(dbname, user, password, host, port)

    def get_park_information(self, park_name) -> Park:
         self._the_cursor.execute(self.__SQL_REQWEST_THE_TABLE, {'the_name': park_name,
                                              'the_rating_category': None, 'the_district': None, 'the_subway': None})

         return Park(*self._the_cursor.fetchall()[0])

    def get_park_list(self, rating_category=None, district=None, subway=None) -> list[Park]:
        self._the_cursor.execute(self.__SQL_REQWEST_THE_TABLE,
                                             {'the_name': None,
                                              'the_rating_category': rating_category,
                                              'the_district': district,
                                              'the_subway': subway
                                              })

        return [Park(*p) for p in self._the_cursor.fetchall()]

    def _get_connection(self):
        return psycopg2.connect(
            dbname=self._dbname,
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port
        )

    def _get_cursor(self):
        return self._the_connection.cursor()


if __name__ == '__main__':
    config = {
            'dbname': 'WarsawPark',
            'user': 'postgres',
            'password': '123',
            'host': 'localhost',
            'port': 5432}

    with PostgresDatabaseConnection('WarsawPark',
                                    'postgres',
                                    '123',
                                    'localhost',
                                    5432) as db:

        print(db.get_park_information('Pole Mokotowskie'))
        print(db.get_park_list(rating_category="B", subway="Ursynów"))

