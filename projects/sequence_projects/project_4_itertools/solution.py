from collections import namedtuple
from csv import reader
from datetime import datetime
from collections import defaultdict, Counter
from itertools import islice, chain, compress, groupby, tee


def _parse_datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')


class PeopleData:
    _EMP_P = 'employment.csv'
    _PER_P = 'personal_info.csv'
    _UPD_P = 'update_status.csv'
    _VEH_P = 'vehicles.csv'
    _TUPLE_PATHS = _EMP_P, _PER_P, _UPD_P, _VEH_P

    _EMP_TN = 'Employment'
    _PER_TN = 'PersonalInfo'
    _UPD_TN = 'UpdateStatus'
    _VEH_TN = 'Vehicles'
    _TUPLE_NAMES = _EMP_TN, _PER_TN, _UPD_TN, _VEH_TN

    _EMP_SEL = True, True, True, True
    _PER_SEL = False, True, True, True, True
    _UPD_SEL = False, True, True
    _VEH_SEL = False, True, True, True
    _TUPLE_SEL = _EMP_SEL, _PER_SEL, _UPD_SEL, _VEH_SEL

    _EMP_DT = str, str, str, str
    _PER_DT = str, str, str, str, str
    _UPD_DT = str, _parse_datetime, _parse_datetime
    _VEH_DT = str, str, str, int
    _TUPLE_DT = _EMP_DT, _PER_DT, _UPD_DT, _VEH_DT

    def _file_headers(self, index: int):
        with open(self._TUPLE_PATHS[index]) as file:
            return next(reader(file))

    def _file_content(self, index: int):
        with open(self._TUPLE_PATHS[index]) as file:
            next(file)  # Skip headers
            yield from reader(file)

    def gen_nt(self, index: int):
        NT = namedtuple(
            self._TUPLE_NAMES[index],
            self._file_headers(index)
        )
        for row in self._file_content(index):
            types = self._TUPLE_DT[index]
            yield NT(*(type_(data) for data, type_ in zip(row, types)))

    def gen_all_nt(self, *, filter_t=lambda arg: True):
        len_ = len(self._TUPLE_DT)

        all_gens_list = [self.gen_nt(i) for i in range(len_)]
        zipped = zip(*all_gens_list)

        headers_list = [self._file_headers(i) for i in range(len_)]
        headers = chain.from_iterable(headers_list)

        selectors = list(chain.from_iterable(self._TUPLE_SEL))

        NT = namedtuple('Data', compress(headers, selectors))
        filtered = filter(
            filter_t, (NT(*compress(chain(*rows), selectors)) for rows in zipped)
        )
        yield from filtered

    def _is_not_stale(self, gender):
        def inner(arg):
            return arg.gender == gender and arg.last_updated > datetime(2017, 3, 1)

        return inner

    def _is_allowed_car(self, makes):
        def inner(arg):
            return arg.vehicle_make in makes
        return inner

    def group_key(self, item):
        return item.vehicle_make

    def grouped_cars(self, gender):
        data = self.gen_all_nt(
            filter_t=lambda arg: arg.last_updated > datetime(2017, 3, 1)
        )
        data_filtered = (row for row in data if row.gender == gender)
        sorted_data_g = sorted(data_filtered, key=self.group_key)
        groups_g = groupby(sorted_data_g, key=self.group_key)
        group_g_counts = ((g[0], len(tuple(g[1]))) for g in groups_g)
        return sorted(group_g_counts, key=lambda arg: arg[1], reverse=True)

    def gen_female_most_popular_car(self):
        return self.grouped_cars('Male')



if __name__ == '__main__':
    from timeit import timeit

    self = PeopleData()
    x = self.gen_female_most_popular_car()
    for y in x:
        print(y)