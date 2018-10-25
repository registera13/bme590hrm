import numpy
import csv
import matplotlib



class DataIO:

    def __init__(self, filename, filetype, outputfile):
        self.filename = filename
        self.filetype = filetype
        self.outputfile = outputfile


    def __int__(self):
        today = datetime.date.today()
        age = today.year - self.birthdate.year

        if today < datetime.date(today.year, self.birthdate.month, self.birthdate.day):
            age -= 1

        return age

person = Person(
    "Jane",
    "Doe",
    datetime.date(1992, 3, 12), # year, month, day
    "No. 12 Short Street, Greenville",
    "555 456 0987",
    "jane.doe@example.com"
)

print(person.name)
print(person.email)
print(person.age())


def ReadData(Filename):
    """
    inintal function to read CVS files

    :param Filename: input the file name of the CVS files
    :return: time, voltage
    """