# attendance.py

# a set of tools to process Roll Call Attendance reports

import csv, sys


class Student:
    def __init__(self, name, id_no) -> None:
        self.name = name
        self.id_no = id_no
        self.record = {}
        self.record["present"] = []
        self.record["absent"] = []
        self.record["late"] = []
        self.record["excused"] = []

def find_student_by_id(students, id):
    for student in students:
        if student.id_no == id:
            return student
    return None


def load_students(filename):
    student_list = set()
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                student_entry = (row["Student ID"], row["Student Name"])
                student_list.add(student_entry)
            line_count += 1
    return student_list

def create_student_objects(student_list):
    students = []
    for (id, name) in student_list:
        students.append(Student(name, id))
    return students

def count_attendance(filename, students):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                student = find_student_by_id(students, row["Student ID"])
                student.record[row["Attendance"]].append(row["Class Date"])
            line_count += 1
    return(students)

def print_summary(students):
    for student in students:
        pres = len(student.record["present"])
        absent = len(student.record["absent"])
        late = len(student.record["late"])
        print(f"{student.name} -- Present: {pres}, Absent: {absent}, Late: {late}")





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ROLLCALL_ATTENDANCEREPORT_FILE")
        sys.exit(-1)

    file = sys.argv[1]
    student_list =load_students(file)
    students = create_student_objects(student_list)
    students = count_attendance(file, students)
    print_summary(students)
