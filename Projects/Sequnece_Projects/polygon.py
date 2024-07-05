import math


class Polygon:
    def __init__(self, n: int, r: int) -> None:
        if n < 3:
            raise ValueError('Polygon has a least 3 edges')
        self._edges = n
        self._vertices = n
        self._r = r

    def __repr__(self):
        return f'Polygon(n={self._edges}, r={self._r})'

    def __eq__(self, other):
        if not isinstance(other, Polygon):
            # raise TypeError("Can only compare Polygon to Polygon")
            return NotImplemented
        return (self._edges, self._r) == (other._edges, other._r)

    def __gt__(self, other):
        if not isinstance(other, Polygon):
            # raise TypeError("Can only compare Polygon to Polygon")
            return NotImplemented
        return self._edges > other._edges

    @property
    def count_vertices(self):
        return self._vertices

    @property
    def count_edges(self):
        return self._edges

    @property
    def circumradius(self):
        return self._r

    @property
    def interior_angle(self) -> float:
        return (self._edges - 2) * 180 / self._edges

    @property
    def edge_length(self) -> float:
        return math.sin(math.pi / self._edges) * self._r * 2

    @property
    def apothem(self) -> float:
        return math.cos(math.pi / self._edges) * self._r

    @property
    def area(self) -> float:
        return self._edges / 2 * self.edge_length * self.apothem

    @property
    def perimeter(self):
        return self._edges * self.edge_length


class Polygons:
    def __init__(self, end: int, radius: int):
        if end < 3:
            raise ValueError('Polygon has a least 3 edges')
        self._end = end
        self._start = 3
        self._r = radius
        self._polygons = tuple(Polygon(i, radius) for i in range(3, end + 1))
        self._max_poly = sorted(self._polygons, key=lambda p: p.area / p.perimeter, reverse=True)

    def __repr__(self):
        return f'Polygons(end={self._end}, radius={self._r})'

    def __len__(self) -> int:
        return self._end - self._start + 1

    def __getitem__(self, item: slice | int):
        return self._polygons[item]

    @property
    def max_efficiency_polygon(self):
        return self._max_poly[0]

