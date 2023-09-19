from turtle import update
import click
import mysql.connector
import time
from tabulate import tabulate
import csv

db = mysql.connector.connect(host='localhost', user='root', password='password123', database = "PGLAB")
cursor = db.cursor()

def logout(userID):
    sql = "DELETE FROM SESSION WHERE User_ID = '%s';" % (userID)
    cursor.execute(sql)

    db.commit()
    click.clear()

def viewStudentGrade(userID, current_sem, current_year):
    # click.clear()

    # studentID = input("Enter Student Enrollment Number: ")

    # l_year = studentID
    
    # year = l_year[0] + l_year[1] + l_year[2] + l_year[3]

    # if year == '2021' and current_year == 2022 and current_sem == 1:
    #     fileName = './transcript_'+studentID+'.txt'
    #     name_fetch_sql = "SELECT First_Name, Last_Name FROM STUDENT WHERE Roll_No = '%s';" % (studentID)
    #     cursor.execute(name_fetch_sql)
    #     name_fetch_res = cursor.fetchall()

    #     for semester in range(1, 3):
    #         table_name = studentID+'_'+str(semester)

    #         sql = "SELECT * FROM %s;" % (table_name)

    #         cursor.execute(sql)

    #         results = cursor.fetchall()
    #         print("\nGrade sheet of semester" + str(semester))
    #         res = tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql')

    #         print(res)


    #     # print("\nFile Path: ", fileName)
    #     input("\nPress any key to continue.")


    click.clear()
    courses_checker_sql = "SELECT COURSES_OFFERED.Course_ID, Course_Title from COURSES_OFFERED INNER JOIN COURSES ON COURSES_OFFERED.Course_ID = COURSES.Course_ID WHERE COURSES_OFFERED.FacultyID = '%s';" % (userID)
    cursor.execute(courses_checker_sql)
    courses_res = cursor.fetchall()

    # print(courses_res[0])

    print("Your Course Offerings are: \n\n")
    print(tabulate(courses_res, headers=['Course ID', 'Course Title'], tablefmt='psql'))

    courseID = input("Enter Course ID for which you want to see Grades: ")

    courseIDList = []
    for val in courses_res:
        courseIDList.append(val[0])

    if courseID not in courseIDList:
        print("\nYou have not offered this course. Please enter valid Course ID that you have offered.")
        input("\nEnter any key to continue.")

        return
    else:
        

        # click.clear()
        
        get_student_list_sql = "SELECT COURSE_REGD.Roll_No, First_Name, Last_Name FROM COURSE_REGD INNER JOIN STUDENT ON COURSE_REGD.Roll_No = STUDENT.Roll_No WHERE COURSE_REGD.Course_ID = '%s';" % (courseID)
        cursor.execute(get_student_list_sql)
        get_student_list_res = cursor.fetchall()

        if get_student_list_res[0][2] != 'nan':
            print(tabulate(get_student_list_res, headers=['Roll No', 'First Name', 'Last Name'], tablefmt='psql'))
        else:
            print(tabulate(get_student_list_res, headers=['Roll No', 'First Name'], tablefmt='psql'))


        # input()




        studentID = input("Enter Student ID whose grade you want to see: ")

        fetch_sql = "SELECT * FROM %s WHERE Roll_No = '%s'" % (courseID, studentID) 
        cursor.execute(fetch_sql)
        fetch_res = cursor.fetchall()

        if fetch_res == []:
            print("\n",studentID, " has not registered in ", courseID)
        else:
            fetch_student_data_sql = "SELECT STUDENT.Roll_No, First_Name, Last_Name, Grades FROM %s INNER JOIN STUDENT ON %s.Roll_No = STUDENT.Roll_No WHERE %s.Roll_No = '%s'" % (courseID, courseID, courseID, studentID)
            cursor.execute(fetch_student_data_sql)
            fetch_student_data = cursor.fetchall()
            print(tabulate(fetch_student_data, headers=['Roll No', 'First Name', 'Last Name', 'Grades'], tablefmt = 'psql'))

        input("Press any key to continue")



def offerNewCourse(userID):
    click.clear()
    courseID = input("Enter Course ID: ")
    cgpa = input("Enter CGPA Constraint (if any): ")

    checker_sql = "SELECT EXISTS(SELECT * FROM COURSES WHERE Course_ID = '%s')" % (courseID)

    cursor.execute(checker_sql)

    res = cursor.fetchall()

    if res[0][0] == 1:  # You can offer the course
        checker_sql_offer = "SELECT EXISTS(SELECT * FROM COURSES_OFFERED WHERE Course_ID = '%s');" % (courseID)

        cursor.execute(checker_sql_offer)
        result = cursor.fetchall()

        # print(result)

        if result[0][0] == 1:  # Means some other faculty has already offered the current course you are trying to offer
            fetch_sql = "SELECT FacultyID FROM COURSES_OFFERED WHERE Course_ID = '%s'" % (courseID)
            cursor.execute(fetch_sql)

            res_fac_id = cursor.fetchall()
            # print(res_fac_id)
            check_sql = "SELECT First_Name, Last_Name FROM FACULTY where FacultyID = '%s'" % (res_fac_id[0][0])
            cursor.execute(check_sql)

            fetch_data = cursor.fetchall()

            print(courseID, "is already offered by ", fetch_data[0][0], fetch_data[0][1])
            print("Please select a different course to offer.")

            time.sleep(3)

            facultyMenu(userID)

        else:
            add_course_sql = "INSERT INTO COURSES_OFFERED VALUES ('%s', '%s', '%s');" % (str(userID), str(courseID), str(cgpa))
            cursor.execute(add_course_sql)

            db.commit()
            db.close()

            print("Course ", courseID, " offered successfully!")
            time.sleep(3)
            return

    else: # You cant offer the course, ask academic office to add the course in the courses list
        print("Sorry, can't offer the course. Ask academic office to add the course in the courses list.")
    


    time.sleep(3)

    return
    # sql = "INSERT INTO COURSES_OFFERED VALUES ('%s', '%s');" % (str(courseID), str(cgpa))


def viewCourseOfferings(userID):
    click.clear()
    view_courses = "SELECT Course_ID, CGPA_Constraint from COURSES_OFFERED WHERE FacultyID = '%s'" % (userID)

    cursor.execute(view_courses)

    results = cursor.fetchall()

    # print(results)
    # print("Course ID\tCourse Title\tL\tT\tP\tS\tC\tCourse Pre-Requisites\tCGPA Constraints")

    for val in results:
        all_course_data = "SELECT * FROM COURSES WHERE Course_ID = '%s';" % (val[0])

        cursor.execute(all_course_data)

        all_data = cursor.fetchall()

        # pre_req = "SELECT * FROM "

        # print(all_data)

        print(tabulate(all_data, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql'))
        

        print("\n\n")


    input("Enter any key to go back to main menu.")

def gradeEntry(userID):
    click.clear()
    courses_checker_sql = "SELECT COURSES_OFFERED.Course_ID, Course_Title from COURSES_OFFERED INNER JOIN COURSES ON COURSES_OFFERED.Course_ID = COURSES.Course_ID WHERE COURSES_OFFERED.FacultyID = '%s';" % (userID)
    cursor.execute(courses_checker_sql)
    courses_res = cursor.fetchall()

    # print(courses_res[0])

    print("Your Course Offerings are: \n\n")
    print(tabulate(courses_res, headers=['Course ID', 'Course Title'], tablefmt='psql'))

    courseID = input("Enter Course ID for which you want to enter Student grades: ")

    courseIDList = []
    for val in courses_res:
        courseIDList.append(val[0])

    if courseID not in courseIDList:
        print("\nYou have not offered this course. Please enter valid Course ID that you have offered.")
        input("\nEnter any key to continue.")

        return
    
    else:
        fileName = "./"+userID + '_' + courseID + '.csv'
        rows = []
        f = open(fileName)
        csvreader = csv.reader(f)

        rows = []
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)

        # print(rows)

        sql_query = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (courseID)
        cursor.execute(sql_query)
        sql_query_res = cursor.fetchall()

        if(sql_query_res[0][0] == 0):
            #create new table
            create_sql_query = "CREATE TABLE %s (Roll_No varchar(20) UNIQUE NOT NULL, Grades varchar(5) NOT NULL);" % (courseID)
            cursor.execute(create_sql_query)

            for val in rows:
                insert_sql_query = "INSERT INTO %s VALUES ('%s', '%s')" % (courseID, val[0], val[1])
                cursor.execute(insert_sql_query)

            db.commit()

            print("Creation of new table and insertion of values successful!!!")

            fetch_names_in_course_regd_sql = "SELECT Roll_No FROM COURSE_REGD WHERE Course_ID = '%s';" % (courseID)
            cursor.execute(fetch_names_in_course_regd_sql)

            fetch_names_in_course_regd_res = cursor.fetchall()

            lst = []
            for val in fetch_names_in_course_regd_res:
                lst.append(val[0])

            # print(lst)

            for rollNo in lst:
                l_year = rollNo
                # print(rollNo)    
                year = l_year[0] + l_year[1] + l_year[2] + l_year[3]

                if year == '2022':
                    fileName = rollNo + '_1' 
                else:
                    fileName = rollNo + '_3'

                checker_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (fileName)
                cursor.execute(checker_sql)

                checker_res = cursor.fetchall()

                if checker_res[0][0] == 0:
                    create_new_table_sql = "CREATE TABLE %s (Course_ID varchar(20) PRIMARY KEY, Course_Title varchar(100), Credits varchar(20), Grade varchar(5));" % (fileName)
                    cursor.execute(create_new_table_sql)

                    fetch_course_details_sql = "SELECT Course_Title, C FROM COURSES WHERE Course_ID = '%s';" % (courseID)
                    cursor.execute(fetch_course_details_sql)

                    fetch_course_details_res = cursor.fetchall()

                    fetch_grades_sql = "SELECT Grades FROM %s WHERE Roll_No = '%s'" % (courseID, rollNo)
                    cursor.execute(fetch_grades_sql)

                    fetch_grades_res = cursor.fetchall()

                    insert_into_new_data = "INSERT INTO %s VALUES('%s', '%s', '%s', '%s');" % (fileName, courseID, fetch_course_details_res[0][0], fetch_course_details_res[0][1], fetch_grades_res[0][0])
                    cursor.execute(insert_into_new_data)

                    db.commit()
                else:
                    fetch_course_details_sql = "SELECT Course_Title, C FROM COURSES WHERE Course_ID = '%s';" % (courseID)
                    cursor.execute(fetch_course_details_sql)

                    fetch_course_details_res = cursor.fetchall()

                    fetch_grades_sql = "SELECT Grades FROM %s WHERE Roll_No = '%s'" % (courseID, rollNo)
                    cursor.execute(fetch_grades_sql)

                    fetch_grades_res = cursor.fetchall()

                    insert_into_new_data = "INSERT INTO %s VALUES('%s', '%s', '%s', '%s');" % (fileName, courseID, fetch_course_details_res[0][0], fetch_course_details_res[0][1], fetch_grades_res[0][0])
                    cursor.execute(insert_into_new_data)

        else:
            #update old table
            for val in rows:
                update_sql_query = "UPDATE %s SET Grades = '%s' WHERE Roll_No = '%s'" % (courseID, val[1], val[0])
                cursor.execute(update_sql_query)

            db.commit()

            print("Updation in Course Grades successful!!!")

            fetch_names_in_course_regd_sql = "SELECT Roll_No FROM COURSE_REGD WHERE Course_ID = '%s';" % (courseID)
            cursor.execute(fetch_names_in_course_regd_sql)

            fetch_names_in_course_regd_res = cursor.fetchall()

            lst = []
            for val in fetch_names_in_course_regd_res:
                lst.append(val[0])

            # print(lst)

            for rollNo in lst:
                l_year = rollNo
    
                year = l_year[0] + l_year[1] + l_year[2] + l_year[3]

                if year == '2022':
                    fileName = rollNo + '_1' 
                else:
                    fileName = rollNo + '_3'

                
                fetch_course_details_sql = "SELECT Course_Title, C FROM COURSES WHERE Course_ID = '%s';" % (courseID)
                cursor.execute(fetch_course_details_sql)

                fetch_course_details_res = cursor.fetchall()

                fetch_grades_sql = "SELECT Grades FROM %s WHERE Roll_No = '%s'" % (courseID, rollNo)
                cursor.execute(fetch_grades_sql)

                fetch_grades_res = cursor.fetchall()

                insert_into_new_data = "UPDATE %s SET Grade = '%s' WHERE Course_ID = '%s';" % (fileName, fetch_grades_res[0][0], courseID)
                cursor.execute(insert_into_new_data)
        db.commit()
        input("Press any key to continue.")


def getStudentListInACourse(userID):
    click.clear()
    courses_checker_sql = "SELECT COURSES_OFFERED.Course_ID, Course_Title from COURSES_OFFERED INNER JOIN COURSES ON COURSES_OFFERED.Course_ID = COURSES.Course_ID WHERE COURSES_OFFERED.FacultyID = '%s';" % (userID)
    cursor.execute(courses_checker_sql)
    courses_res = cursor.fetchall()

    # print(courses_res[0])

    print("Your Course Offerings are: \n\n")
    print(tabulate(courses_res, headers=['Course ID', 'Course Title'], tablefmt='psql'))

    courseID = input("Enter Course ID for which you want to see Student List: ")

    courseIDList = []
    for val in courses_res:
        courseIDList.append(val[0])

    if courseID not in courseIDList:
        print("\nYou have not offered this course. Please enter valid Course ID that you have offered.")
        input("\nEnter any key to continue.")

        return
    
    else:
        get_student_list_sql = "SELECT COURSE_REGD.Roll_No, First_Name, Last_Name FROM COURSE_REGD INNER JOIN STUDENT ON COURSE_REGD.Roll_No = STUDENT.Roll_No WHERE COURSE_REGD.Course_ID = '%s';" % (courseID)
        cursor.execute(get_student_list_sql)
        get_student_list_res = cursor.fetchall()

        if get_student_list_res[0][2] != 'nan':
            print(tabulate(get_student_list_res, headers=['Roll No', 'First Name', 'Last Name'], tablefmt='psql'))
        else:
            print(tabulate(get_student_list_res, headers=['Roll No', 'First Name'], tablefmt='psql'))


        input("Enter any key to continue.")



def facultyMenu(userID, current_sem, current_year):

    sql = "select First_Name, Last_Name from FACULTY where FacultyID = '%s'" % (userID)
    cursor.execute(sql)

    results = cursor.fetchall()

    # print(results[0])

    while(1):
        click.clear()
        if results[0][1] != 'nan':
            print("********** Welcome ", results[0][0], results[0][1], " **********")
        else:
            print("********** Welcome ", results[0][0], " **********")
        print("1. View Grade of Student")
        print("2. Offer a new Course")
        print("3. Grade Entry")
        print("4. View Course Offerings")
        print("5. Get Student list in a course")
        print("6. Logout")

        choice = input()

        if(choice == str(1)):
            viewStudentGrade(userID, current_sem, current_year)
        elif(choice == str(2)):
            offerNewCourse(userID)
        elif(choice == str(3)):
            gradeEntry(userID)
        elif(choice == str(4)):
            viewCourseOfferings(userID)
        elif(choice == str(5)):
            getStudentListInACourse(userID)
        elif(choice == str(6)):
            logout(userID)
            return
        else:
            input("\n\nWrong Input. Please try again! \n Press any key to continue")


# facultyMenu()
