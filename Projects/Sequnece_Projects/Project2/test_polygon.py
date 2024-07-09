import math

import pytest
from polygon import Polygon, Polygons


@pytest.fixture
def triangle():
    return Polygon(3, 1)

@pytest.fixture
def square():
    return Polygon(4, 1)


def is_close(a, b) -> bool:
    return math.isclose(a, b, rel_tol=0.001, abs_tol=0.001)


def test_not_a_polygon():
    with pytest.raises(ValueError):
        Polygon(1, 1)
    with pytest.raises(ValueError):
        Polygon(2, 1)


def test_representation_polygon(triangle):
    string_rep = str(triangle)
    polygon = eval(string_rep)
    assert isinstance(polygon, Polygon)


def test_initialization(triangle):
    assert triangle._edges == 3
    assert triangle._vertices == 3
    assert triangle._r == 1


def test_interior_angle(triangle):
    assert triangle.interior_angle == 60


def test_equality(triangle):
    assert triangle == triangle
    assert triangle != Polygon(4, 1)


def test_greater_than(triangle):
    assert not (triangle < triangle)
    assert triangle < Polygon(4, 1)
    assert Polygon(4, 1) > triangle


def test_max_area_polygon():
    polygons = Polygons(5, 1)
    assert is_close(polygons.max_area, 2.377)


def test_max_area_square(square: Polygon):
    assert is_close(square.area, 2.0)


def test_square_perimeter(square: Polygon):
    assert is_close(square.perimeter, 4 * math.sqrt(2))


def test_polygons():
    polygons = Polygons(5, 1)
    assert len(polygons) == 3


def test_not_a_polygons():
    with pytest.raises(ValueError):
        Polygons(1, 1)
    with pytest.raises(ValueError):
        Polygons(2, 1)


def test_representation_polygons():
    string_rep = str(Polygons(3, 1))
    polygon = eval(string_rep)
    assert isinstance(polygon, Polygons)


def test_polygons_len():
    assert len(Polygons(3, 1)) == 1
    assert len(Polygons(5, 1)) == 3


def test_best_ration_polygon():
    polygons = Polygons(10, 1)
    assert polygons.max_efficiency_polygon is polygons[-1]


def test_best_poly():
    p = Polygon(10*9, 1)
    assert is_close(p.area, math.pi)