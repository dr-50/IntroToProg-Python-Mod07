# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   Devon Ross, 11/23/2026, Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

students: list = []
menu_choice: str = ''


class Person:
    """
    A class to represent a student.

    ChangeLog: (Who, WHen, What)
    DevonRoss, 11/23/2026, created class

    Properties:
    - first_name: string data as first name
    - last_name: string data as last name
    """
    first_name: str = ""
    last_name: str = ""

    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":
            self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("Invalid last name. Name should not contain numbers")

    def __str__(self):
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """
    A class to represent a student inheriting from Person.

    ChangeLog: (Who, WHen, What)
    DevonRoss, 11/23/2026, created class

    Properties:
    - first_name: string data as first name
    - last_name: string data as last name
    - course_name: string data as course name
    """
    def __init__(self, first_name="", last_name: str="", course_name: str=""):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.course_name}"

class FileProcessor:
    """
    A collection of functions that process the file data

    ChangeLog: (Who, When, What)
    Devon Ross, 11/16/2026, Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str):
        """This function reads data from file

        ChangeLog: (Who, When, What)
        Devon Ross, 11/16/2026, Created function

        :param file_name: string data as file name

        :return: list
        """
        file = None
        try:

            file = open(file_name, "r")
            json_student = json.load(file)
            for row in json_student:
                student_obj = Student(first_name=row["FirstName"],
                                      last_name=row["LastName"],
                                      course_name=row["CourseName"])
                students.append(student_obj)


        except FileNotFoundError as e:
            IO.output_error_message("File must exist before running this program!", e)
        except Exception as e:
            IO.output_error_message("There was a non-specific error!", e)
        finally:
            if file is not None and file.closed == False:
                file.close()

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """This function writes current data to file

        :param file_name: string data as file name
        :param student_data: list of dictionaries as student data
        """

        json_students = []
        for student in student_data:
            student_dict = {"FirstName": student.first_name,
                            "LastName": student.last_name,
                            "CourseName": student.course_name}
            json_students.append(student_dict)

        file = open(FILE_NAME, "w")
        json.dump(json_students, file, indent=4)
        # check if a file object exists and is still open
        if file is not None and file.closed == False:
            file.close()

        print("The following data was saved to file!")
        for student in students:
            print(f"Student {student.first_name} {student.last_name} is enrolled in "
                  f"{student.course_name}")


class IO:
    """
    A collection of functions that handle input output

    ChangeLog: (Who, When, What)
    Devon Ross, 11/16/2026, Created Class
    """

    @staticmethod
    def output_menu(menu: str):
        """This function displays menu options

        :return: none
        """
        print(menu)
        print()  # extra space for UI appearance

    @staticmethod
    def input_menu_choice():
        """This function accepts user menu selection

        :return: string number as choice
        """
        choice = "0"
        try:
            choice = input("Please select an option: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please choose only 1, 2, 3, or 4")
        except Exception as e:
                IO.output_menu(e.__str__())
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """This function prints student courses

        :param student_data: list of dictionaries as student data
        """
        print("-" * 50)
        for student in student_data:
            print(f"{student.first_name},{student.last_name},{student.course_name}")
            # print(f"{student['FirstName']},{student['LastName']},"
            #       f"{student['CourseName']}")

    @staticmethod
    def output_error_message(message: str, error: Exception = None):
        """This function prints error message

        :param message: string message to display
        :param error: Exception to display
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep="\n")

    @staticmethod
    def input_student_data(student_data: list):
        """This function accepts user input values and appends them to
        students list

        :param student_data: list of dictionaries as student data
        """
        try:
            #collect user inputs
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.strip():
                raise ValueError("The first name should not be empty.")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.strip():
                raise ValueError("The last name should not be empty.")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Enter the course's name: ")
            if not course_name.strip():
                raise ValueError("The course name should not be empty.")
            student_data_row = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            student_obj = Student(first_name=student_data_row["FirstName"],
                                  last_name=student_data_row["LastName"],
                                  course_name=student_data_row["CourseName"])
            students.append(student_obj)
        except ValueError as e:
            IO.output_error_message(e.__str__())
        except Exception as e:
            IO.output_error_message("There was a non-specific error!", e)


#-- End of function definitions --#

#-- Beginning of the main body of script --#
# #Read data from file on initial start of program
# FileProcessor.read_data_from_file(FILE_NAME, [])
FileProcessor.read_data_from_file(file_name=FILE_NAME)

while True:

    #present menu
    IO.output_menu(menu=MENU)
    #store user selection and validate
    menu_choice = IO.input_menu_choice()

    #User input of student data
    if menu_choice == "1":
        IO.input_student_data(students)
        continue

    #Present current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    #save current data
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)
        continue

    #Stop the loop
    elif menu_choice == "4":
        break

print("End of Program.\nThank you!")