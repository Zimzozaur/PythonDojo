import Importing
import Importing.package as pack

import Importing.models as models

import helpers


pack.antimath()
pack._Classy()

john_post = models.Post()
john_posts = models.Posts()
john = models.User()


print("\nThis Module\n")
for key, value in dict(globals()).items():
    print(f'{key}: {value}')

print("\nImporting\n")
for key, value in Importing.__dict__.items():
    print(f'{key}')

print("\npackage\n")
for key, value in pack.__dict__.items():
    print(f'{key}')

print("\nmodels\n")
for key, value in models.__dict__.items():
    if key == '__builtins__':
        continue
    print(f'{key}: {value}')

print("\nhelpers\n")
for key, value in helpers.__dict__.items():
    print(f'{key}')


import asyncio
import email
