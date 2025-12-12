def check_uniqueness(new_item, attr, items):
    attr_list = [getattr(item, attr) for item in items]
    if getattr(new_item, attr) in attr_list:
        item_name = 'Курс' if attr == 'code' else new_item.get_role()
        raise ValueError(f'{item_name} с таким {attr} уже существует')
    
    
class Person:
    def __init__(self, name, id, email):
        self.name = name
        self.id = id
        self.email = email
    
    def get_role(self):
        return 'Роль человека'
    

class Student(Person):
    def __init__(self, name, id, email, courses=None):
        super().__init__(name, id, email)
        self.courses = courses or []

    def get_role(self):
        return 'Студент'

    def enroll(self, course):
        check_uniqueness(self, 'id', course.students)
        self.courses.append(course)
        course.students.append(self)
        if course.grades.get(self) is None:
            course.grades[self] = []

    def get_gpa(self):
        courses_gpa = [
            sum(course.grades[self]) / len(course.grades[self]) 
            for course in self.courses if self in course.students and course.grades[self]
            ]
        total_gpa = sum(courses_gpa) / len(courses_gpa) if courses_gpa else 0
        return round(total_gpa, 2)
    

class Professor(Person):
    def __init__(self, name, id, email, department, courses_taught=None):
        super().__init__(name, id, email)
        self.department = department
        self.courses_taught = courses_taught or []

    def get_role(self):
        return 'Профессор'

    def assign_course(self, course):
        check_uniqueness(course, 'code', self.courses_taught)
        self.courses_taught.append(course)
        course.professor = self


class Course:
    def __init__(self, code, name, credits):
        self.code = code
        self.name = name
        self.credits = credits
        self.professor = None
        self.students = []
        self.grades = {}
    
    def add_student(self, student):
        student.enroll(self)

    def record_grade(self, student, grade):
        if self.grades.get(student) is None:
            raise KeyError('Студент не существует или не записан на курс')
        self.grades[student].append(grade)

    def get_average_grade(self):
        avg_grades = [
            sum(self.grades[student]) / len(self.grades[student])
            for student in self.students if self.grades[student]
            ]
        total_avg_grade = sum(avg_grades) / len(avg_grades) if avg_grades else 0
        return round(total_avg_grade, 2)
    

class University:
    def __init__(self):
        self.students = []
        self.professors = []
        self.courses = []

    def add_student(self, student):
        check_uniqueness(student, 'id', self.students)
        self.students.append(student)
    
    def add_professor(self, professor):
        check_uniqueness(professor, 'id', self.professors)
        self.professors.append(professor)

    def create_course(self, course):
        check_uniqueness(course, 'code', self.courses)
        self.courses.append(course)

    def generate_report(self):
        courses = f'Курсы:{''.join(
            f'\n\t{course.code} {course.name}'
            for course in self.courses
            )}'
        professors = f'Профессора:{''.join(
            f'\n\t{prof.name}: {', '.join(
                f'{course.code} {course.name}'
                for course in prof.courses_taught
                )}'
            for prof in self.professors
            )}'
        students = f'Студенты:{''.join(
            f'\n\t{student.name} (GPA {student.get_gpa()})'
            + (f': {', '.join(
                f'{course.code} {course.name}'
                for course in student.courses
                )}' if student.courses else '')
            for student in self.students
            )}'
        return f'\n{courses}\n\n{professors}\n\n{students}\n'


# Тесты
uni = University()
prof = Professor("Иванов", "P001", "mail1@example.com", "Математика")
uni.add_professor(prof)
course = Course("MATH101", "Математика", 3)
uni.create_course(course)
prof.assign_course(course)
student1 = Student("Петров", "S001", "mail2@example.com")
student2 = Student("Сидоров", "S002", "mail3@example.com")
uni.add_student(student1)
uni.add_student(student2)
course.add_student(student1)
course.record_grade(student1, 4)
course.record_grade(student1, 5)
print(uni.generate_report())