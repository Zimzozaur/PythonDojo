from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, ValidationError


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
    )

    manufacturer: str
    series_name: str
    type_: AutomobileType
    is_electric: bool = False
    manufactured_date: date
    base_msrp_usd: float
    vin: str
    number_of_doors: int = 4
    registration_country: str | None = None
    license_plate: str | None = None


if __name__ == '__main__':
    data_json = '''
    {
        "manufacturer": " BMW ",
        "series_name": " M4 ",
        "type_": "Convertible",
        "manufactured_date": "2023-01-01",
        "base_msrp_usd": 93300,
        "vin": " 1234567890 "
    }
    '''
    data_json_expected_serialization = {
        'manufacturer': 'BMW',
        'series_name': 'M4',
        'type_': AutomobileType.convertible,
        'is_electric': False,
        'manufactured_date': date(2023, 1, 1),
        'base_msrp_usd': 93300.0,
        'vin': '1234567890',
        'number_of_doors': 4,
        'registration_country': None,
        'license_plate': None
    }

    auto = Automobile.model_validate_json(data_json)
    assert auto.model_dump() == data_json_expected_serialization

    data_json = '''
    {
        "manufacturer": " BMW ",
        "series_name": " M4 ",
        "type_": "Convertibl",
        "manufactured_date": "2023-01-01",
        "base_msrp_usd": 93300,
        "vin": " 1234567890 "
    }
    '''
    try:
        Automobile.model_validate_json(data_json)
    except ValidationError as ex:
        print("Passed wrong type_ literal")

    data_json = '''
    {
        "manufacturer": null,
        "series_name": " M4 ",
        "type_": "Convertible",
        "manufactured_date": "2023-01-01",
        "base_msrp_usd": 93300,
        "vin": " 1234567890 "
    }
    '''
    try:
        Automobile.model_validate_json(data_json)
    except ValidationError as ex:
        print("Passed wrong manufacturer data type")