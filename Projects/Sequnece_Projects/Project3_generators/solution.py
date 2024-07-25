from datetime import datetime
from collections import namedtuple, Counter


def str_to_date(string):
    date_format = '%m/%d/%Y'
    return datetime.strptime(string, date_format).date()


types = int, str, str, str, str_to_date, int, str, str, str


def cast_types(row):
    return (type_(col) for type_, col in zip(types, row))


def split_row_of_data(row):
    return str(row).strip().split(',')


def create_named_tuple(row_of_data, named_tuple):
    return named_tuple(*cast_types(row_of_data))


def return_named_tuple(row, named_tuple_):
    list_ = split_row_of_data(row)
    return create_named_tuple(list_, named_tuple_)


def gen_named_tuples_from_csv(file):
    with open(file) as f:
        headers = next(f)  # Skip first row
        ParkingTicket = namedtuple(
            'ParkingTicket',
            [
                header.strip().lower().replace(' ', '_')
                for header in headers.split(',')
            ]
        )
        for row in f:
            yield return_named_tuple(row, ParkingTicket)


def violation_count_by_make(tickets):
    return Counter(car.vehicle_make for car in tickets)


def sort_violations(gen):
    return sorted(gen, key=lambda tup: tup[1], reverse=True)


if __name__ == '__main__':
    cars_gen = gen_named_tuples_from_csv('nyc_parking_tickets_extract.csv')
    counted = violation_count_by_make(cars_gen)
    tupled = ((key, value) for key, value in counted.items())
    for name, value in sort_violations(tupled):
        print(f'{name}: {value}')

