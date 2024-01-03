from .Model_ID import Model_ID
from typing import Any


class Address(Model_ID):
    def __init__(
        self,
        schema: str,
        id: int = None,
        street: str = None,
        number: str = None,
        zipcode: str = None,
        complement: str = None,
        neighborhood: str = None,
        city_district: str = None,
        city: str = None,
        county: str = None,
        state: str = None,
        state_code: str = None,
        country: str = None,
        country_code: str = None,
        latitude: float = None,
        longitude: float = None,
    ) -> None:
        super().__init__(schema, id)
        self.street = street
        self.number = number
        self.zipcode = zipcode
        self.complement = complement
        self.neighborhood = neighborhood
        self.city_district = city_district
        self.city = city
        self.county = county
        self.state = state
        self.state_code = state_code
        self.country = country
        self.country_code = country_code
        self.latitude = latitude
        self.longitude = longitude

    def copy(self) -> "Address":
        return Address(
            schema=self.schema,
            id=self.id,
            street=self.street,
            number=self.number,
            zipcode=self.zipcode,
            complement=self.complement,
            neighborhood=self.neighborhood,
            city_district=self.city_district,
            city=self.city,
            county=self.county,
            state=self.state,
            state_code=self.state_code,
            country=self.country,
            country_code=self.country_code,
            latitude=self.latitude,
            longitude=self.longitude,
        )

    def from_dict(self, dictionary: dict[str, Any]) -> None:
        super().from_dict(dictionary)
        self.street = dictionary.pop("street", None)
        self.number = dictionary.pop("number", None)
        self.zipcode = dictionary.pop("zipcode", None)
        self.complement = dictionary.pop("complement", None)
        self.neighborhood = dictionary.pop("neighborhood", None)
        self.city_district = dictionary.pop("city_district", None)
        self.city = dictionary.pop("city", None)
        self.county = dictionary.pop("county", None)
        self.state = dictionary.pop("state", None)
        self.state_code = dictionary.pop("state_code", None)
        self.country = dictionary.pop("country", None)
        self.country_code = dictionary.pop("country_code", None)
        self.latitude = dictionary.pop("latitude", None)
        self.longitude = dictionary.pop("longitude", None)

        return self.copy()

    def to_dict(
        self, ignore_none: bool = False, include_id: bool = False
    ) -> dict[str, Any]:
        self_dict = {
            "street": self.street,
            "number": self.number,
            "zipcode": self.zipcode,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city_district": self.city_district,
            "city": self.city,
            "county": self.county,
            "state": self.state,
            "state_code": self.state_code,
            "country": self.country,
            "country_code": self.country_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

        result = super().to_dict(ignore_none, include_id)
        if ignore_none:
            for key, value in self_dict.items():
                if value is not None:
                    result[key] = value
        else:
            result.update(self_dict)

        return result

    @property
    def street(self) -> None | str:
        return self._street

    @street.setter
    def street(self, street: None | str) -> None:
        if street is None:
            self._street = None
            return

        try:
            street = str(street)
            if len(street) > 100:
                raise ValueError(
                    f"Street should not be longer than 100 characters, but the argument has {len(street)}"
                )

            self._street = street
        except TypeError:
            raise TypeError(f"Street should be a String, not a {type(street)}")

    @property
    def number(self) -> None | str:
        return self._number

    @number.setter
    def number(self, number: None | str) -> None:
        if number is None:
            self._number = None
            return

        try:
            number = str(number)
            if len(number) > 10:
                raise ValueError(
                    f"Number should not be longer than 10 characters, but the argument has {len(number)}"
                )

            self._number = number
        except TypeError:
            raise TypeError(f"Number should be a String, not a {type(number)}")

    @property
    def zipcode(self) -> None | str:
        return self._zipcode

    @zipcode.setter
    def zipcode(self, zipcode: None | str) -> None:
        if zipcode is None:
            self._zipcode = None
            return

        try:
            zipcode = str(zipcode)
            if len(zipcode) > 20:
                raise ValueError(
                    f"Zipcode should not be longer than 20 characters, but the argument has {len(zipcode)}"
                )

            self._zipcode = zipcode
        except TypeError:
            raise TypeError(f"Zipcode should be a String, not a {type(zipcode)}")

    @property
    def complement(self) -> None | str:
        return self._complement

    @complement.setter
    def complement(self, complement: None | str) -> None:
        if complement is None:
            self._complement = None
            return

        try:
            complement = str(complement)
            if len(complement) > 30:
                raise ValueError(
                    f"Complement should not be longer than 30 characters, but the argument has {len(complement)}"
                )

            self._complement = complement
        except TypeError:
            raise TypeError(f"Complement should be a String, not a {type(complement)}")

    @property
    def neighborhood(self) -> None | str:
        return self._neighborhood

    @neighborhood.setter
    def neighborhood(self, neighborhood: None | str) -> None:
        if neighborhood is None:
            self._neighborhood = None
            return

        try:
            neighborhood = str(neighborhood)
            if len(neighborhood) > 30:
                raise ValueError(
                    f"Neighborhood should not be longer than 30 characters, but the argument has {len(neighborhood)}"
                )

            self._neighborhood = neighborhood
        except TypeError:
            raise TypeError(
                f"Neighborhood should be a String, not a {type(neighborhood)}"
            )

    @property
    def city_district(self) -> None | str:
        return self._city_district

    @city_district.setter
    def city_district(self, city_district: None | str) -> None:
        if city_district is None:
            self._city_district = None
            return

        try:
            city_district = str(city_district)
            if len(city_district) > 60:
                raise ValueError(
                    f"City district should not be longer than 60 characters, but the argument has {len(city_district)}"
                )

            self._city_district = city_district
        except TypeError:
            raise TypeError(
                f"City district should be a String, not a {type(city_district)}"
            )

    @property
    def city(self) -> None | str:
        return self._city

    @city.setter
    def city(self, city: None | str) -> None:
        if city is None:
            self._city = None
            return

        try:
            city = str(city)
            if len(city) > 60:
                raise ValueError(
                    f"City should not be longer than 60 characters, but the argument has {len(city)}"
                )

            self._city = city
        except TypeError:
            raise TypeError(f"City should be a String, not a {type(city)}")

    @property
    def county(self) -> None | str:
        return self._county

    @county.setter
    def county(self, county: None | str) -> None:
        if county is None:
            self._county = None
            return

        try:
            county = str(county)
            if len(county) > 120:
                raise ValueError(
                    f"County should not be longer than 120 characters, but the argument has {len(county)}"
                )

            self._county = county
        except TypeError:
            raise TypeError(f"County should be a String, not a {type(county)}")

    @property
    def state(self) -> None | str:
        return self._state

    @state.setter
    def state(self, state: None | str) -> None:
        if state is None:
            self._state = None
            return

        try:
            state = str(state)
            if len(state) > 60:
                raise ValueError(
                    f"State should not be longer than 60 characters, but the argument has {len(state)}"
                )

            self._state = state
        except TypeError:
            raise TypeError(f"State should be a String, not a {type(state)}")

    @property
    def state_code(self) -> None | str:
        return self._state_code

    @state_code.setter
    def state_code(self, state_code: None | str) -> None:
        if state_code is None:
            self._state_code = None
            return

        try:
            state_code = str(state_code)
            if len(state_code) > 3:
                raise ValueError(
                    f"State code should not be longer than 3 characters, but the argument has {len(state_code)}"
                )

            self._state_code = state_code
        except TypeError:
            raise TypeError(f"State code should be a String, not a {type(state_code)}")

    @property
    def country(self) -> None | str:
        return self._country

    @country.setter
    def country(self, country: None | str) -> None:
        if country is None:
            self._country = None
            return

        try:
            country = str(country)
            if len(country) > 60:
                raise ValueError(
                    f"Country should not be longer than 60 characters, but the argument has {len(country)}"
                )

            self._country = country
        except TypeError:
            raise TypeError(f"Country should be a String, not a {type(country)}")

    @property
    def country_code(self) -> None | str:
        return self._country_code

    @country_code.setter
    def country_code(self, country_code: None | str) -> None:
        if country_code is None:
            self._country_code = None
            return

        try:
            country_code = str(country_code)
            if len(country_code) > 2:
                raise ValueError(
                    f"Country code should not be longer than 2 characters, but the argument has {len(country_code)}"
                )

            self._country_code = country_code
        except TypeError:
            raise TypeError(
                f"Country code should be a String, not a {type(country_code)}"
            )

    @property
    def latitude(self) -> None | float:
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: None | float) -> None:
        if latitude is None:
            self._latitude = None
            return

        try:
            latitude = float(latitude)
            self._latitude = latitude
        except TypeError:
            raise TypeError(f"Latitude should be Float, not a {type(latitude)}")

    @property
    def longitude(self) -> None | float:
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: None | float) -> None:
        if longitude is None:
            self._longitude = None
            return

        try:
            longitude = float(longitude)
            self._longitude = longitude
        except TypeError:
            raise TypeError(f"Longitude should be Float, not a {type(longitude)}")
