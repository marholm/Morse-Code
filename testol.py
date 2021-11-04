#Tester OOP i Python

#Lager generisk klasse

class Student:
    'Basic class for all students at NTNU'

    studCount = 0

    def __init__(self, studnr, degree, email):
        self.studnr = studnr
        self.degree = degree
        self.email = email
        Student.studCount += 1

    def access_Student(self):
        print('Studentnr: ',  self.studnr, ', Degree: ', self.degree, ', Email: ', self.email)

    def access_Studcount(self):
        print('Studentcount: ', Student.studCount)


stud1 = Student(1234, 'CompSci', '1234@mail.com')
stud1.access_Student()
stud1.access_Studcount()
print()
stud2 = Student(5678, 'Literature', '5678@mail.com')
stud2.access_Student()
stud2.access_Studcount()
print()
a = Student.__doc__
print(a)
