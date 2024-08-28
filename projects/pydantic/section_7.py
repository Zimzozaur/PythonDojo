from datetime import date
from enum import Enum
from uuid import uuid4, UUID
from typing import Annotated, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    UUID4,
    StringConstraints
)
from pydantic.alias_generators import to_camel

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


class AutomobileType(Enum):
    sedan = 'Sedan'
    coupe = 'Coupe'
    convertible = 'Convertible'
    suv = 'SUV'
    truck = 'Truck'


class Automobile(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_default=True,
        validate_assignment=True,
        alias_generator=to_camel
    )

    id_: UUID4 = Field(default_factory=uuid4, alias="id")
    manufacturer: BoundedString
    series_name: BoundedString
    type_: AutomobileType = Field(alias="type")
    is_electric: bool = False
    manufactured_date: date = Field(
        validation_alias="completionDate", ge=date(1980, 1, 1)
    )
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD",
        serialization_alias="baseMSRPUSD"
    )
    top_features: BoundedList[BoundedString] = None
    vin: BoundedString
    number_of_doors: int = Field(
        default=4, validation_alias="doors", ge=2, le=4, multiple_of=2
    )
    registration_country: BoundedString | None = None
    license_plate: BoundedString | None = None

    @field_serializer("manufactured_date", when_used='json-unless-none')
    def serialize_manufactured_date(self, dt: date):
        return dt.strftime("%Y/%m/%d")


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
        "registrationCountry": "France",
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
        'registrationCountry': 'France',
        'licensePlate': 'AAA-BBB'
    }

    model = Automobile.model_validate(data)
    assert model.model_dump(by_alias=True) == expected_serialized_by_alias


    class Model(BaseModel):
        model_config = ConfigDict(
            extra='forbid',
            str_strip_whitespace=True,
            validate_default=True,
            validate_assignment=True,
            alias_generator=to_camel
        )
        top_features: BoundedList[BoundedString] = None

    Model()