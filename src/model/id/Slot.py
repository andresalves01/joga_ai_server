from typing import Any
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

    def copy(self) -> "Slot":
        return Slot(
            schema=self.schema,
            id=self.id,
            reservation_datetime=self.reservation_datetime,
            price=self.price,
            cancellation_datetime=self.cancellation_datetime,
            user_id=self.user_id,
            court_id=self.court_id,
        )

    def from_dict(self, dictionary: dict[str, Any]) -> None:
        super().from_dict(dictionary)
        self.reservation_datetime = dictionary.pop("reservation_datetime", None)
        self.price = dictionary.pop("price", None)
        self.cancellation_datetime = dictionary.pop("cancellation_datetime", None)
        self.court_id = dictionary.pop("court_id", None)
        self.user_id = dictionary.pop("user_id", None)

    def to_dict(
        self, ignore_none: bool = False, include_id: bool = False
    ) -> dict[str, Any]:
        self_dict = {
            "reservation_datetime": self.reservation_datetime,
            "price": self.price,
            "cancellation_datetime": self.cancellation_datetime,
            "user_id": self.user_id,
            "court_id": self.court_id,
        }

        result = super().to_dict(ignore_none, include_id)
        if ignore_none:
            for key, value in self_dict.items():
                if value is not None:
                    result[key] = value

        return result

    @property
    def reservation_datetime(self) -> None | datetime:
        return self._reservation_datetime

    @reservation_datetime.setter
    def reservation_datetime(self, reservation_datetime: None | datetime | str) -> None:
        if reservation_datetime is None:
            self._reservation_datetime = None
            return

        if isinstance(reservation_datetime, datetime):
            self._reservation_datetime = reservation_datetime
        elif isinstance(reservation_datetime, str):
            try:
                self._reservation_datetime = datetime.strptime(
                    reservation_datetime, "%Y-%m-%d %H:%M:%S %Z"
                )
            except Exception:
                raise ValueError(
                    "Reservation datetime should have %Y-%m-%d %H:%M:%S %Z format as a String"
                )
        else:
            raise TypeError(
                f"Reservation datetime should be a String or a Datetime, not {type(reservation_datetime)}"
            )

    @property
    def price(self) -> None | float:
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        if price is None:
            self._price = None
            return

        try:
            price = float(price)
            if price < 50.0:
                raise ValueError("Price should be greater than or equal to 50.0")

            self._price = price
        except TypeError:
            raise TypeError(f"Price should be a Float, not {type(price)}")

    @property
    def cancellation_datetime(self) -> datetime:
        return self._cancellation_datetime

    @cancellation_datetime.setter
    def cancellation_datetime(self, cancellation_datetime: datetime) -> None:
        if cancellation_datetime is None:
            self._cancellation_datetime = None
            return
        elif self.reservation_datetime is None:
            raise AttributeError(
                "Cancellation datetime cannot be defined if reservation datetime is None."
            )

        # Converts a string into a datetime.
        try:
            if isinstance(cancellation_datetime, str):
                cancellation_datetime = datetime.strptime(
                    cancellation_datetime, "%Y-%m-%d %H:%M:%S %Z"
                )
        except Exception:
            raise ValueError(
                "Cancellation datetime should have %Y-%m-%d %H:%M:%S %Z format as a String"
            )

        # If cancellation_datetime reaches this point as the correct type, checks if it is
        # previous than reservation datetime
        if isinstance(cancellation_datetime, datetime):
            if cancellation_datetime > self.reservation_datetime:
                raise ValueError(
                    "Cancellation datetime should be previous than reservation datetime"
                )

            self._cancellation_datetime = cancellation_datetime
        else:
            raise TypeError(
                f"Cancellation datetime should be a String or a Datetime, not {type(cancellation_datetime)}"
            )

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        if user_id is None:
            self._user_id = user_id
            return

        try:
            user_id = int(user_id)
            if user_id < 0:
                raise ValueError("User ID should be greater than zero")

            self._user_id = user_id
        except TypeError:
            raise TypeError(f"User ID should be an integer, not {type(user_id)}")

    @property
    def court_id(self) -> int:
        return self._court_id

    @court_id.setter
    def court_id(self, court_id: int) -> None:
        if court_id is None:
            self._court_id = court_id
            return

        try:
            court_id = int(court_id)
            if court_id < 0:
                raise ValueError("Court ID should be greater than zero")

            self._court_id = court_id
        except TypeError:
            raise TypeError(f"Court ID should be an integer, not {type(court_id)}")
