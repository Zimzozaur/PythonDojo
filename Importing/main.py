import Importing
import Importing.package as pack

pack.antimath()
pack._Classy()

print("\nThis Module\n")
for key, value in dict(globals()).items():
    print(f'{key}: {value}')

print("\nImporting\n")
for key, value in Importing.__dict__.items():
    print(f'{key}')

print("\npackage\n")
for key, value in pack.__dict__.items():
    print(f'{key}')



