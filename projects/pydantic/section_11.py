from datetime import date
from enum import Enum
from uuid import uuid4, UUID
from functools import cached_property
from typing import Annotated, TypeVar

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    computed_field,
    Field,
    field_serializer,
    field_validator,
    UUID4,
    PlainSerializer,
    StringConstraints,
    ValidationInfo,
)
from pydantic.alias_generators import to_camel


def validate_registration_country(country: "Country"):
    country = country.lower()
    if country not in countries:
        raise ValueError("Country not supported")
    return countries[country][0]


def serialize_date(self, dt: date):
    return dt.strftime("%Y/%m/%d")


T = TypeVar("T")

BoundedString = Annotated[
    str,
    StringConstraints(
        min_length=2, max_length=50
    )
]

BoundedList = Annotated[
    list[T],
    Field(min_length=1, max_length=5)
]

Country = Annotated[
    str,
    StringConstraints(
        min_length=2, max_length=50, strip_whitespace=True
    ),
    AfterValidator(validate_registration_country)
]

CustomDate = Annotated[
    date,
    PlainSerializer(serialize_date, when_used='json-unless-none')
]

countries = {
    "australia": ("Australia", "AUS"),
    "canada": ("Canada", "CAN"),
    "china": ("China", "CHN"),
    "france": ("France", "FRA"),
    "germany": ("Germany", "DEU"),
    "india": ("India", "IND"),
    "mexico": ("Mexico", "MEX"),
    "norway": ("Norway", "NOR"),
    "pakistan": ("Pakistan", "PAK"),
    "san marino": ("San Marino", "SMR"),
    "sanmarino": ("San Marino", "SMR"),
    "spain": ("Spain", "ESP"),
    "sweden": ("Sweden", "SWE"),
    "united kingdom": ("United Kingdom", "GBR"),
    "uk": ("United Kingdom", "GBR"),
    "great britain": ("United Kingdom", "GBR"),
    "britain": ("United Kingdom", "GBR"),
    "us": ("United States of America", "USA"),
    "united states": ("United States of America", "USA"),
    "usa": ("United States of America", "USA"),
}

country_code_lookup = {
    name: code for name, code in countries.values()
}


class AutomobileType(Enum):
    sedan = 'Sedan'
    coupe = 'Coupe'
    convertible = 'Convertible'
    suv = 'SUV'
    truck = 'Truck'


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_default=True,
        validate_assignment=True,
        alias_generator=to_camel,
    )


class RegistrationCountry(CustomBaseModel):
    name: Country | None = None

    @computed_field
    @cached_property
    def code3(self) -> str:
        return country_code_lookup[self.name]


class Automobile(CustomBaseModel):
    id_: UUID4 = Field(default_factory=uuid4, alias="id")
    manufacturer: BoundedString
    series_name: BoundedString
    type_: AutomobileType = Field(alias="type")
    is_electric: bool = Field(default=False, repr=False)
    manufactured_date: CustomDate = Field(
        validation_alias="completionDate", ge=date(1980, 1, 1),
        repr=False
    )
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD",
        serialization_alias="baseMSRPUSD",
        repr=False
    )
    top_features: BoundedList[BoundedString] = Field(default=None, repr=False)
    vin: BoundedString = Field(repr=False)
    number_of_doors: int = Field(
        default=4, validation_alias="doors", ge=2, le=4, multiple_of=2,
        repr=False
    )
    registration_country: RegistrationCountry | None = Field(
        default=None, repr=False
    )
    registration_date: CustomDate | None = Field(default=None, repr=False)
    license_plate: BoundedString | None = Field(default=None, repr=False)

    @field_validator("registration_date")
    def validate_registration_date(cls, registration: date, values: ValidationInfo):
        data = values.data
        key = "manufactured_date"
        if key in data and data[key] <= registration:
            return registration
        raise ValueError("manufactured_date cannot be earlier than registration_date")


if __name__ == '__main__':
    data = {
        "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
        "manufacturer": "BMW",
        "seriesName": "M4 Competition xDrive",
        "type": "Convertible",
        "isElectric": False,
        "completionDate": "2023-01-01",
        "msrpUSD": 93_300,
        "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
        "vin": "1234567890",
        "doors": 2,
        "registrationCountry": {"name": "us"},
        "registrationDate": "2023-06-01",
        "licensePlate": "AAA-BBB"
    }

    expected_serialized_by_alias = {
        'id': UUID('c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7'),
        'manufacturer': 'BMW',
        'seriesName': 'M4 Competition xDrive',
        'type': AutomobileType.convertible,
        'isElectric': False,
        'manufacturedDate': date(2023, 1, 1),
        'baseMSRPUSD': 93300.0,
        'topFeatures': ['6 cylinders', 'all-wheel drive', 'convertible'],
        'vin': '1234567890',
        'numberOfDoors': 2,
        'registrationCountry': {
            'name': 'United States of America',
            'code3': 'USA'
        },
        'registrationDate': date(2023, 6, 1),
        'licensePlate': 'AAA-BBB'
    }

    model = Automobile.model_validate(data)

    print(model.model_dump(by_alias=True), end='\n\n')
    print(expected_serialized_by_alias)

    assert model.model_dump(by_alias=True) == expected_serialized_by_alias


