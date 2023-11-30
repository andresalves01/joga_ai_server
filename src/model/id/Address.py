from .Model_ID import Model_ID


class Address(Model_ID):
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
        self.latitude = latitude
        self.longitude = longitude

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
