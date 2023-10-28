from typing import Any, Dict
from .Model_ID import Model_ID
from datetime import datetime


class Slot(Model_ID):
    def __init__(
        self,
        schema: str,
        id: int = None,
        reservation_datetime: datetime = None,
        price: float = None,
        cancellation_datetime: datetime = None,
        user_id: int = None,
        court_id: int = None,
    ) -> None:
        super().__init__(schema, id)
        self.reservation_datetime = reservation_datetime
        self.price = price
        self.cancellation_datetime = cancellation_datetime
        self.user_id = user_id
        self.court_id = court_id

    def copy(self):
        return Slot(
            self.schema,
            self.id,
            self.reservation_datetime,
            self.price,
            self.cancellation_datetime,
            self.user_id,
            self.court_id,
        )

    @property
    def reservation_datetime(self) -> datetime:
        return self.__reservation_datetime

    @reservation_datetime.setter
    def reservation_datetime(self, value: datetime) -> None:
        self.__reservation_datetime = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value is None or value >= 0.0:
            self.__price = value
        else:
            raise Exception("Invalid price")

    @property
    def cancellation_datetime(self) -> datetime:
        return self.__cancellation_datetime

    @cancellation_datetime.setter
    def cancellation_datetime(self, value: datetime) -> None:
        if (
            self.reservation_datetime is None
            or value is None
            or value <= self.reservation_datetime
        ):
            self.__cancellation_datetime = value
        else:
            raise Exception("Invalid cancelation date")

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__user_id = value
        else:
            raise Exception("Invalid User ID")

    @property
    def court_id(self) -> int:
        return self.__court_id

    @court_id.setter
    def court_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__court_id = value
        else:
            raise Exception("Invalid Court ID")
