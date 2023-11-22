from typing import Any, Dict
from .Model_ID import Model_ID
import re


class User(Model_ID):
    def __init__(
        self,
        schema: str,
        name: str = None,
        email: str = None,
        id: int = None,
        password: str = None,
        ssn: str = None,
        phone_number: str = None,
        profile_pic_url: str = None,
        address_id: int = None,
    ) -> None:
        super().__init__(schema, id)
        self.name = name
        self.email = email
        self.password = password
        self.ssn = ssn
        self.phone_number = phone_number
        self.profile_pic_url = profile_pic_url
        self.address_id = address_id

    def copy(self) -> Model_ID:
        return User(
            self.schema,
            self.name,
            self.email,
            self.id,
            self.password,
            self.ssn,
            self.phone_number,
            self.profile_pic_url,
            self.address_id,
        )

    def attributes_to_dict(self, ignore_None: bool = False) -> dict[str, Any]:
        dictionary = super().attributes_to_dict(ignore_None)
        dictionary.pop("password")

        return dictionary

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if value is None or (
            re.match(r"^[a-zA-Z]{2,}([ ][a-zA-Z]+)*$", value) and len(value) <= 100
        ):
            self.__name = value
        else:
            raise Exception("Invalid name")

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        if value is None or (
            len(value) <= 320
            and re.match(
                r"^[a-zA-Z][a-zA-Z0-9]*([._][a-zA-Z0-9]{1,})*@[a-zA-Z][a-zA-Z0-9]*([.-][a-zA-Z0-9]{1,}){1,}$",
                value,
            )
        ):
            self.__email = value
        else:
            raise Exception("Invalid e-mail")

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str):
        if value is None or len(value) <= 100:
            self.__password = value
        else:
            raise Exception("Invalid password")

    @property
    def ssn(self) -> str:
        return self.__ssn

    @ssn.setter
    def ssn(self, value: str) -> None:
        if value is None or re.match(r"^[0-9]{11}$", value):
            self.__ssn = value
        else:
            raise Exception("Invalid Social Security Number")

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        if value is None or re.match(r"^[0-9]{11}$", value):
            self.__phone_number = value
        else:
            raise Exception("Invalid Social Security Number")

    @property
    def profile_pic_url(self) -> str:
        return self.__profile_pic_url

    @profile_pic_url.setter
    def profile_pic_url(self, value: str) -> None:
        if value is None or len(value) <= 2080:
            self.__profile_pic_url = value
        else:
            raise Exception("Invalid profile picture url")

    @property
    def address_id(self) -> int:
        return self.__address_id

    @address_id.setter
    def address_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__address_id = value
        else:
            raise Exception("Invalid Address ID")
