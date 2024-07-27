# helpers

from .calculator import Calc


def say_hello(name):
    return f'Hello {name}'


def factorial(n: int) -> int:
    if n <= 1:
        return 1
    factorial_result = 1
    for i in range(1, n + 1):
        factorial_result *= i
    return factorial_result
