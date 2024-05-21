# run.py

# print(f'loading run.py: __name__ = {__name__}')

import timing

code = '[x**2 for x in range(10**3)]'

result = timing.timeit(code, 10**1)
print(result)

