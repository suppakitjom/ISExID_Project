# rename all files in animal_bgs2 to have uppercase first letter
# and lowercase rest of name, including lowercase .png
import os
for file in os.listdir('animal_bgs2'):
    x = file.split('.')
    x[1] = x[1].lower()
    os.rename(f'animal_bgs2/{file}', f'animal_bgs2/{x[0]}.{x[1]}')
