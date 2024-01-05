from typing import Any
from .Model_Address_ID import Model_Address_ID
import re


class User(Model_Address_ID):
    def __init__(
        self,
        schema: str,
        id: int = None,
        name: str = None,
        email: str = None,
        password: str = None,
        ssn: str = None,
        phone_number: str = None,
        profile_pic_url: str = None,
        address_id: int = None,
    ) -> None:
        super().__init__(schema, id, address_id)
        self.name = name
        self.email = email
        self.password = password
        self.ssn = ssn
        self.phone_number = phone_number
        self.profile_pic_url = profile_pic_url

    def copy(self) -> "User":
        return User(
            schema=self.schema,
            id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            ssn=self.ssn,
            phone_number=self.phone_number,
            profile_pic_url=self.profile_pic_url,
            address_id=self.address_id,
        )

    def from_dict(self, dictionary: dict[str, Any]) -> "User":
        super().from_dict(dictionary)
        self.name = dictionary.pop("name", None)
        self.email = dictionary.pop("email", None)
        self.password = dictionary.pop("password", None)
        self.ssn = dictionary.pop("ssn", None)
        self.phone_number = dictionary.pop("phone_number", None)
        self.profile_pic_url = dictionary.pop("profile_pic_url", None)

        return self.copy()

    def to_dict(self, ignore_none: bool = False) -> dict[str, Any]:
        self_dict = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "ssn": self.ssn,
            "phone_number": self.phone_number,
            "profile_pic_url": self.profile_pic_url,
        }

        result = super().to_dict(ignore_none)
        if ignore_none:
            for key, value in self_dict.items():
                if value is not None:
                    result[key] = value
        else:
            result.update(self_dict)

        return result

    @property
    def name(self) -> None | str:
        return self._name

    @name.setter
    def name(self, name: None | str) -> None:
        if name is None:
            self._name = None
            return

        try:
            name = str(name)
            if len(name) > 100:
                raise ValueError(
                    "Name length should not be greater than 100 characters."
                )

            self._name = name
        except TypeError:
            raise TypeError(f"Name should be a String, not a {type(name)}")

    @property
    def email(self) -> None | str:
        return self._email

    @email.setter
    def email(self, email: None | str) -> None:
        if email is None:
            self._email = None
            return

        try:
            email = str(email)
            if len(email) > 320 or not re.match(
                r"^[a-zA-Z][a-zA-Z0-9]*([._][a-zA-Z0-9]{1,})*@[a-zA-Z][a-zA-Z0-9]*([.-][a-zA-Z0-9]{1,}){1,}$",
                email,
            ):
                raise ValueError(
                    "Email length should not be greater than 320 characters and match its regex."
                )

            self._email = email
        except TypeError:
            raise TypeError(f"Email should be a String, not a {type(email)}")

    @property
    def password(self) -> None | str:
        return self._password

    @password.setter
    def password(self, password: str):
        if password is None:
            self._password = None
            return

        try:
            password = str(password)
            if len(password) > 100:
                raise ValueError(
                    "Password length should not be greater than 100 characters."
                )

            self._password = password
        except TypeError:
            raise TypeError(f"Password should be a String, not a {type(password)}")

    @property
    def ssn(self) -> None | str:
        return self._ssn

    @ssn.setter
    def ssn(self, ssn: str) -> None:
        if ssn is None:
            self._ssn = None
            return

        try:
            ssn = str(ssn)
            if len(ssn) > 20 or not re.match(
                r"^[0-9]{11}$",
                ssn,
            ):
                raise ValueError(
                    "SSN length should not be greater than 20 characters and match its regex."
                )

            self._ssn = ssn
        except TypeError:
            raise TypeError(f"SSN should be a String, not a {type(ssn)}")

    @property
    def phone_number(self) -> None | str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number: None | str) -> None:
        if phone_number is None:
            self._phone_number = None
            return

        try:
            phone_number = str(phone_number)
            if len(phone_number) > 20 or not re.match(
                r"^[0-9]{11}$",
                phone_number,
            ):
                raise ValueError(
                    "Phone number length should not be greater than 20 characters and match its regex."
                )

            self._phone_number = phone_number
        except TypeError:
            raise TypeError(
                f"Phone number should be a String, not a {type(phone_number)}"
            )

    @property
    def profile_pic_url(self) -> None | str:
        return self._profile_pic_url

    @profile_pic_url.setter
    def profile_pic_url(self, profile_pic_url: None | str) -> None:
        if profile_pic_url is None:
            self._profile_pic_url = None
            return

        try:
            profile_pic_url = str(profile_pic_url)
            if len(profile_pic_url) > 2080:
                raise ValueError(
                    "Profile Pic Url length should not be greater than 2080 characters."
                )

            self._profile_pic_url = profile_pic_url
        except TypeError:
            raise TypeError(
                f"Profile Pic Url should be a String, not a {type(profile_pic_url)}"
            )
