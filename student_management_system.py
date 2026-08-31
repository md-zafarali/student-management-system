"""
Student Management System
--------------------------
Ek simple CLI based Student Management System jo student ka data
add, view, update, delete aur search karne deta hai.
Data CSV file (students.csv) mein save hota hai, so data permanent
rehta hai (program band karne ke baad bhi).
"""

import csv
import os

FILENAME = "students.csv"
FIELDS = ["Roll No", "Name", "Age", "Class", "Marks"]


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def initialize_file():
    """Agar CSV file exist nahi karti, to naya file banayega with header."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)


def read_all_students():
    """CSV se saare students ko list of dictionaries mein return karta hai."""
    students = []
    with open(FILENAME, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(row)
    return students


def write_all_students(students):
    """Poori list ko wapas CSV mein likh deta hai (update/delete ke liye)."""
    with open(FILENAME, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)


def roll_no_exists(roll_no, students):
    """Check karta hai ki given roll number pehle se data mein hai ya nahi."""
    return any(s["Roll No"] == str(roll_no) for s in students)


# ---------------------------------------------------------
# Core Features
# ---------------------------------------------------------

def add_student():
    print("\n--- Add New Student ---")
    students = read_all_students()

    roll_no = input("Roll No: ").strip()
    if roll_no_exists(roll_no, students):
        print(f"Error: Roll No {roll_no} already exists!")
        return

    name = input("Name: ").strip()
    age = input("Age: ").strip()
    student_class = input("Class: ").strip()
    marks = input("Marks: ").strip()

    if not (roll_no and name and age and student_class and marks):
        print("Error: Koi bhi field khali nahi ho sakta!")
        return

    new_student = {
        "Roll No": roll_no,
        "Name": name,
        "Age": age,
        "Class": student_class,
        "Marks": marks,
    }

    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow(new_student)

    print(f"Student '{name}' successfully add ho gaya!")


def view_all_students():
    print("\n--- All Students ---")
    students = read_all_students()

    if not students:
        print("Koi student record nahi mila.")
        return

    print(f"{'Roll No':<10}{'Name':<20}{'Age':<6}{'Class':<10}{'Marks':<8}")
    print("-" * 54)
    for s in students:
        print(f"{s['Roll No']:<10}{s['Name']:<20}{s['Age']:<6}{s['Class']:<10}{s['Marks']:<8}")


def search_student():
    print("\n--- Search Student ---")
    roll_no = input("Search karne ke liye Roll No enter karein: ").strip()
    students = read_all_students()

    for s in students:
        if s["Roll No"] == roll_no:
            print("\nStudent Mil Gaya:")
            for key, value in s.items():
                print(f"{key}: {value}")
            return

    print(f"Roll No {roll_no} ka koi student nahi mila.")


def update_student():
    print("\n--- Update Student ---")
    roll_no = input("Update karne ke liye Roll No enter karein: ").strip()
    students = read_all_students()

    found = False
    for s in students:
        if s["Roll No"] == roll_no:
            found = True
            print(f"Current Data: {s}")
            print("\nNaya data enter karein (khali chhodne par purana data rahega):")

            new_name = input(f"Name [{s['Name']}]: ").strip()
            new_age = input(f"Age [{s['Age']}]: ").strip()
            new_class = input(f"Class [{s['Class']}]: ").strip()
            new_marks = input(f"Marks [{s['Marks']}]: ").strip()

            if new_name:
                s["Name"] = new_name
            if new_age:
                s["Age"] = new_age
            if new_class:
                s["Class"] = new_class
            if new_marks:
                s["Marks"] = new_marks

            break

    if found:
        write_all_students(students)
        print("Student data successfully update ho gaya!")
    else:
        print(f"Roll No {roll_no} ka koi student nahi mila.")


def delete_student():
    print("\n--- Delete Student ---")
    roll_no = input("Delete karne ke liye Roll No enter karein: ").strip()
    students = read_all_students()

    filtered_students = [s for s in students if s["Roll No"] != roll_no]

    if len(filtered_students) == len(students):
        print(f"Roll No {roll_no} ka koi student nahi mila.")
        return

    confirm = input(f"Kya aap sach mein Roll No {roll_no} delete karna chahte hain? (yes/no): ").strip().lower()
    if confirm == "yes":
        write_all_students(filtered_students)
        print("Student successfully delete ho gaya!")
    else:
        print("Delete cancel kar diya gaya.")


def show_statistics():
    print("\n--- Class Statistics ---")
    students = read_all_students()

    if not students:
        print("Koi data available nahi hai.")
        return

    total = len(students)
    marks_list = [float(s["Marks"]) for s in students]
    avg_marks = sum(marks_list) / total
    highest = max(students, key=lambda s: float(s["Marks"]))
    lowest = min(students, key=lambda s: float(s["Marks"]))

    print(f"Total Students : {total}")
    print(f"Average Marks  : {avg_marks:.2f}")
    print(f"Highest Marks  : {highest['Name']} ({highest['Marks']})")
    print(f"Lowest Marks   : {lowest['Name']} ({lowest['Marks']})")


# ---------------------------------------------------------
# Menu / Main Program
# ---------------------------------------------------------

def show_menu():
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Show Statistics")
    print("7. Exit")
    print("======================================")


def main():
    initialize_file()

    while True:
        show_menu()
        choice = input("Apna choice enter karein (1-7): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            print("Program band ho raha hai. Dhanyawad!")
            break
        else:
            print("Galat choice! Kripya 1 se 7 tak koi number enter karein.")


if __name__ == "__main__":
    main()
