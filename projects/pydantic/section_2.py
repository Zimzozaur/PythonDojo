from datetime import date

from pydantic import BaseModel


class Automobile(BaseModel):
    manufacturer: str
    series_name: str
    type_: str
    is_electric: bool = False
    manufactured_date: date
    base_msrp_usd: float
    vin: str
    number_of_doors: int = 4
    registration_country: str | None = None
    license_plate: str | None = None


if __name__ == '__main__':
    data = {
        "manufacturer": "BMW",
        "series_name": "M4",
        "type_": "Convertible",
        "is_electric": False,
        "manufactured_date": "2023-01-01",
        "base_msrp_usd": 93_300,
        "vin": "1234567890",
        "number_of_doors": 2,
        "registration_country": "France",
        "license_plate": "AAA-BBB",
    }

    data_expected_serialization = {
        'manufacturer': 'BMW',
        'series_name': 'M4',
        'type_': 'Convertible',
        'is_electric': False,
        'manufactured_date': date(2023, 1, 1),
        'base_msrp_usd': 93_300,
        'vin': '1234567890',
        'number_of_doors': 2,
        'registration_country': 'France',
        'license_plate': 'AAA-BBB',
    }

    a1 = Automobile.model_validate(data)
    assert a1.model_dump() == data_expected_serialization

    data_json = '''
    {
        "manufacturer": "BMW",
        "series_name": "M4",
        "type_": "Convertible",
        "manufactured_date": "2023-01-01",
        "base_msrp_usd": 93300,
        "vin": "1234567890"
    }
    '''

    data_json_expected_serialization = {
        'manufacturer': 'BMW',
        'series_name': 'M4',
        'type_': 'Convertible',
        'is_electric': False,
        'manufactured_date': date(2023, 1, 1),
        'base_msrp_usd': 93_300,
        'vin': '1234567890',
        'number_of_doors': 4,
        'registration_country': None,
        'license_plate': None,
    }

    a2 = Automobile.model_validate_json(data_json)
    assert a2.model_dump() == data_json_expected_serialization

