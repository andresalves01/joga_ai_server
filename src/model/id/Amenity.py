from typing import Any
from .Model_ID import Model_ID


class Amenity(Model_ID):
    def __init__(
        self, schema: str, name: str = None, id: int = None, icon_url: str = None
    ) -> None:
        super().__init__(schema, id)
        self.name = name
        self.icon_url = icon_url

    def copy(self) -> "Amenity":
        return Amenity(
            schema=self.schema, name=self.name, id=self.id, icon_url=self.icon_url
        )

    def from_dict(self, dictionary: dict[str, Any]) -> "Amenity":
        super().from_dict(dictionary)
        self.name = dictionary.pop("name", None)
        self.icon_url = dictionary.pop("icon_url", None)

        return self.copy()

    def to_dict(
        self, ignore_none: bool = False, include_id: bool = False
    ) -> dict[str, Any]:
        self_dict = {"name": self.name, "icon_url": self.icon_url}

        result = super().to_dict(ignore_none, include_id)
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
            if len(name) > 50:
                raise ValueError(
                    f"Name length should be less than 50 characters, but it has {len(name)}"
                )

            self._name = name
        except TypeError:
            raise TypeError(f"Name should be a String, not a {type(name)}")

    @property
    def icon_url(self) -> str:
        return self._icon_url

    @icon_url.setter
    def icon_url(self, icon_url: None | str) -> None:
        if icon_url is None:
            self._icon_url = None
            return

        try:
            icon_url = str(icon_url)
            if len(icon_url) > 2080:
                raise ValueError(
                    f"Icon Url length should be less than 2080 characters, but it has {len(icon_url)}"
                )
            self._icon_url = icon_url
        except TypeError:
            raise TypeError(f"Icon Url should be a String, not a {type(icon_url)}")
