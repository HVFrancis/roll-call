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
                if student is not None:
                    student.record[row["Attendance"]].append(row["Class Date"])
            line_count += 1
    return(students)

def print_summary(students):
    for student in students:
        pres = len(student.record["present"])
        late = len(student.record["late"])
        absent = len(student.record["absent"])
        #print(f"{student.name} -- Present: {pres}, Absent: {absent}, Late: {late}")
        #print(f"{student.name} Absent Days {student.record['absent']}")
        print(f"{student.name} -- Present: {pres}, Absent: {absent}, Date Last attendend: {student.record['present'][-1]}")

def return_cvs(students):
    ret_string = "Student Name, Days Present, Days Absent, Days Late, Last Date Attended\n"
    for student in students:
        pres = len(student.record["present"])
        absent = len(student.record["absent"])
        late = len(student.record["late"])
        last_date = student.record['present'][-1]
        student_line = f"{student.name}, {pres}, {absent}, {late}, {last_date}"
        ret_string += student_line + "\n"
    return ret_string

def count_total_days(filename):
    date_set = set()
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                #student = find_student_by_id(students, row["Student ID"])
                date_set.add(row["Class Date"])
            line_count += 1
    return(len(date_set))



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ROLLCALL_ATTENDANCEREPORT_FILE")
        sys.exit(-1)

    file = sys.argv[1]
    student_list = load_students(file)
    students = create_student_objects(student_list)
    students = count_attendance(file, students)
#    print_summary(students)
    print(return_cvs(students))
    print(count_total_days(file))
