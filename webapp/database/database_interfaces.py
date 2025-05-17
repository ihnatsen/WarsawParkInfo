from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Park:
    name: str
    attractions: str
    area: float
    rating: float
    rating_category: str
    districts: str
    subways: str


class DatabaseInterface(ABC):

    def __init__(self, dbname, user, password, host, port):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._the_connection = self._get_connection()
        self._the_cursor = self._get_cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._the_connection.rollback()
        else:
            self._the_connection.commit()
        self._the_cursor.close()
        self._the_connection.close()

    @abstractmethod
    def get_park_information(self, park_name) -> Park:
        pass

    @abstractmethod
    def get_park_list(self, rating_category, metro, rating) -> list[str]:
        pass

    @abstractmethod
    def _get_cursor(self):
        pass

    @abstractmethod
    def _get_connection(self):
        pass
