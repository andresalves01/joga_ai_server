from typing import Any
from .Model_ID import Model_ID


class Photo(Model_ID):
    def __init__(
        self,
        schema: str,
        id: int = None,
        url: str = None,
        court_id: int = None,
        presentaton_order: int = None,
    ) -> None:
        super().__init__(schema, id)
        self.url = url
        self.court_id = court_id
        self.presentaton_order = presentaton_order

    def copy(self) -> "Photo":
        return Photo(
            schema=self.schema,
            id=self.id,
            url=self.url,
            court_id=self.court_id,
            presentaton_order=self.presentation_order,
        )

    def from_dict(self, dictionary: dict[str, Any]) -> "Photo":
        super().from_dict(dictionary)
        self.url = dictionary.pop("url", None)
        self.court_id = dictionary.pop("court_id", None)
        self.presentaton_order = dictionary.pop("presentation_order", None)

        return self.copy()

    def to_dict(self, ignore_none: bool = False) -> dict[str, Any]:
        self_dict = {
            "url": self.url,
            "court_id": self.court_id,
            "presentation_order": self.presentation_order,
        }
        result = super().to_dict()

        if ignore_none:
            for key, value in result.items():
                if value is not None:
                    result[key] = value
        else:
            result.update(self_dict)

        return result

    @property
    def url(self) -> None | str:
        return self._url

    @url.setter
    def url(self, url: None | str) -> None:
        if url is None:
            self._url = None
            return

        try:
            url = str(url)
            if len(url) > 2080:
                raise ValueError(
                    f"Url length should be less than 2080 characters, but it has {len(url)}"
                )

            self._url = url
        except TypeError:
            raise TypeError(f"Url should be a String, not a {type(url)}")

    @property
    def court_id(self) -> None | int:
        return self._court_id

    @court_id.setter
    def court_id(self, court_id: None | int) -> None:
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

    @property
    def presentation_order(self) -> None | int:
        return self._presentation_order

    @presentation_order.setter
    def presentation_order(self, presentation_order: None | int) -> None:
        if presentation_order is None:
            self._presentation_order = presentation_order
            return

        try:
            presentation_order = int(presentation_order)
            if presentation_order < 0:
                raise ValueError("Presentation Order should be greater than zero")

            self._presentation_order = presentation_order
        except TypeError:
            raise TypeError(
                f"Presentation order should be an integer, not {type(presentation_order)}"
            )
