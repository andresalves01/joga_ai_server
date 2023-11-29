import time
from .Model_ID import Model_ID
from geopy.geocoders import Nominatim
import re


class Address(Model_ID):
    last_request_time_ = 0.0

    def __init__(
        self,
        schema: str,
        id: int = None,
        street: str = None,
        number: int = None,
        zipcode: str = None,
        complement: str = None,
        block: str = None,
        city_district: str = None,
        city: str = None,
        state: str = None,
        country: str = None,
        latitude: float = None,
        longitude: float = None,
    ) -> None:
        super().__init__(schema=schema, id=id)
        self.street = street
        self.number = number
        self.zipcode = zipcode
        self.complement = complement
        self.block = block
        self.city_district = city_district
        self.city = city
        self.state = state
        self.country = country

        self.geolocator_ = Nominatim(user_agent="joga_ai")

        self.latitude = latitude
        self.longitude = longitude
        self.set_coordinates()

    @classmethod
    def get_last_request_time(cls):
        return cls.last_request_time_

    @classmethod
    def set_last_request_time(cls):
        cls.last_request_time = time.time()

    def copy(self) -> Model_ID:
        return Address(
            self.schema,
            self.id,
            self.street,
            self.number,
            self.zipcode,
            self.complement,
            self.block,
            self.city_district,
            self.city,
            self.state,
            self.country,
            self.latitude,
            self.longitude,
        )

    def from_json(self, dictonary: dict[str, any]) -> dict[str, any]:
        valueToReturn = super().from_json(dictonary)
        if self.get_search_address():
            self.set_coordinates()
        elif self.latitude and self.longitude:
            self.set_address()

        return valueToReturn

    def from_fetched_row(self, row: tuple[any]) -> None:
        super().from_fetched_row(row)
        if self.get_search_address():
            self.set_coordinates()
        elif self.latitude and self.longitude:
            self.set_address()
        else:
            print("Address can't be completed using geopy.")

    def get_search_address(self) -> str | None:
        search_address = (
            f"{self.street}, {self.block}, {self.city}, {self.state}, {self.country}"
        )
        objectToReturn = (
            search_address if search_address != "None, None, None, None, None" else None
        )

        return objectToReturn

    def set_coordinates(self) -> None:
        if (self.latitude and self.longitude) or not self.get_search_address():
            return

        time_elapsed = time.time() - Address.get_last_request_time()
        if time_elapsed < 1.0:
            time.sleep(1.0 - time_elapsed)

        location = self.geolocator_.geocode(self.get_search_address())
        Address.set_last_request_time()

        if location is not None:
            self.latitude = location.latitude if not self.latitude else self.latitude
            self.longitude = (
                location.longitude if not self.longitude else self.longitude
            )
        else:
            print("Coordintes could not be completed with geopy.")

    def set_address(self) -> None:
        time_elapsed = time.time() - last_request_time_
        if time_elapsed < 1.0:
            time.sleep(1.0 - time_elapsed)

        if self.latitude and self.longitude:
            location = self.geolocator_.reverse(f"{self.latitude}, {self.longitude}")
            last_request_time_ = time.time()

            if location:
                address_data = location.raw.get("address", {})

                self.street = address_data.get("road")
                self.zipcode = address_data.get("postcode").replace("-", "")
                self.block = address_data.get("suburb")
                self.city_district = address_data.get("city_district")
                self.city = address_data.get("city")
                self.state = address_data.get("state")
                self.country = address_data.get("country")

    @property
    def street(self) -> str:
        return self.__street

    @street.setter
    def street(self, value: str) -> None:
        self.__street = value

    @property
    def number(self) -> int:
        return self.__number

    @number.setter
    def number(self, value: int) -> None:
        if value is None or value >= 0:
            self.__number = value
        else:
            raise Exception("Invalid number")

    @property
    def zipcode(self) -> str:
        return self.__zipcode

    @zipcode.setter
    def zipcode(self, value: str) -> None:
        self.__zipcode = value

    @property
    def complement(self) -> str:
        return self.__complement

    @complement.setter
    def complement(self, value: str) -> None:
        self.__complement = value

    @property
    def block(self) -> str:
        return self.__block

    @block.setter
    def block(self, value: str) -> None:
        self.__block = value

    @property
    def city_district(self) -> str:
        return self.__city_district

    @city_district.setter
    def city_district(self, value: str) -> None:
        self.__city_district = value

    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, value: str) -> None:
        self.__city = value

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str) -> None:
        self.__state = value

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self, value: str) -> None:
        self.__country = value

    @property
    def latitude(self) -> float:
        return self.__latitude

    @latitude.setter
    def latitude(self, value: float) -> None:
        self.__latitude = value

    @property
    def longitude(self) -> float:
        return self.__longitude

    @longitude.setter
    def longitude(self, value: float) -> None:
        self.__longitude = value
