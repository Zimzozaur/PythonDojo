import math


class Polygon:
    def __init__(self, n: int, r: int) -> None:
        if n < 3:
            raise ValueError('Polygon has a least 3 edges')
        self._edges = n
        self._vertices = n
        self._r = r

        # LAZY PROPERTIES
        self._interior_angle = None
        self._edge_length = None
        self._apothem = None
        self._area = None
        self._perimeter = None

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
        if not self._interior_angle:
            self._interior_angle = (self._edges - 2) * 180 / self._edges
        return self._interior_angle

    @property
    def edge_length(self) -> float:
        if not self._edge_length:
            self._edge_length = math.sin(math.pi / self._edges) * self._r * 2
        return self._edge_length

    @property
    def apothem(self) -> float:
        if not self._apothem:
            self._apothem = math.cos(math.pi / self._edges) * self._r
        return self._apothem

    @property
    def area(self) -> float:
        if not self._area:
            self._area = self._edges / 2 * self.edge_length * self.apothem
        return self._area

    @property
    def perimeter(self):
        if not self._perimeter:
            return self._edges * self.edge_length
        return self._perimeter


class Polygons:
    def __init__(self, end: int, radius: int):
        if end < 3:
            raise ValueError('Polygon has a least 3 edges')
        self._end = end
        self._start = 3
        self._r = radius

    def __repr__(self):
        return f'Polygons(end={self._end}, radius={self._r})'

    def __len__(self) -> int:
        return self._end - self._start + 1

    def __iter__(self):
        return self.PolygonIterator(self._end, self._r)

    class PolygonIterator:
        def __init__(self, polygons: int, radius: int):
            self.polygons: int = polygons
            self.radius: int = radius
            self.i = 3

        def __iter__(self):
            return self

        def __next__(self):
            if self.i > self.polygons:
                raise StopIteration
            res = Polygon(self.i, self.radius)
            self.i += 1
            return res
