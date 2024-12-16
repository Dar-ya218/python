## File Handling ###

import xml
import csv
import json
import os

# .txt file

# Leer, escribir y sobrescribir si ya existe
txt_file = open("Intermediate/my_file.txt", "w+")

txt_file.write(
    "Mi nombre es Dasha\nMi apellido es Boch\n30 años\nY mi lenguaje preferido es Python")

# print(txt_file.read())
print(txt_file.read(10))
print(txt_file.readline())
print(txt_file.readline())
for line in txt_file.readlines():
    print(line)

txt_file.write("\nAunque también me gusta React")
print(txt_file.readline())

txt_file.close()

with open("Intermediate/my_file.txt", "a") as my_other_file:
    my_other_file.write("\nY Swift")

# os.remove("Intermediate/my_file.txt")

# .json file


json_file = open("Intermediate/my_file.json", "w+")

json_test = {
    "name": "Dasha",
    "surname": "Boch",
    "age": 30,
    "languages": ["Python", "Swift", "React"],
    "website": "https://boch.dev"}

json.dump(json_test, json_file, indent=2)

json_file.close()

with open("Intermediate/my_file.json") as my_other_file:
    for line in my_other_file.readlines():
        print(line)

json_dict = json.load(open("Intermediate/my_file.json"))
print(json_dict)
print(type(json_dict))
print(json_dict["name"])

# .csv file


csv_file = open("Intermediate/my_file.csv", "w+")

csv_writer = csv.writer(csv_file)
csv_writer.writerow(["name", "surname", "age", "language", "website"])
csv_writer.writerow(["Dasha", "Boch", 30, "Python", "https://boch.dev"])
csv_writer.writerow(["Roswell", "", 2, "COBOL", ""])

csv_file.close()

with open("Intermediate/my_file.csv") as my_other_file:
    for line in my_other_file.readlines():
        print(line)

# .xlsx file
# import xlrd # Debe instalarse el módulo

# .xml file
