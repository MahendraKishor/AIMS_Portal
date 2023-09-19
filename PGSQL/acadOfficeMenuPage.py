from cmath import nan
import click
import mysql.connector
import time
from tabulate import tabulate
import os
import pandas as pd

db = mysql.connector.connect(host='localhost', user='root', password='password123', database = "PGLAB")
cursor = db.cursor()

def logout(userID):
    sql = "DELETE FROM SESSION WHERE User_ID = '%s';" % (userID)
    cursor.execute(sql)

    db.commit()
    click.clear()


def downloadTranscript(current_sem, current_year):
    click.clear()

    student_list_sql = "SELECT Roll_No, First_Name, Last_Name FROM STUDENT;"
    cursor.execute(student_list_sql)

    student_list_res = cursor.fetchall()

    print(tabulate(student_list_res, headers = ['Enrollment Number', 'First Name', 'Last Name'], tablefmt='psql'))

    studentID = input("Enter Student Enrollment Number: ")

    l_year = studentID
    
    year = l_year[0] + l_year[1] + l_year[2] + l_year[3]

    if year == '2022':
        table_name = studentID+'_1'

        table_check_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (table_name)
        cursor.execute(table_check_sql)

        table_check_res = cursor.fetchall()

        if table_check_res[0][0] == 0:
            print("Gradesheet doesn't exist. Please try again with valid input.")
            input("Press any key to continue")

            return
        else:
            sql = "SELECT * FROM %s;" % (table_name)
            cursor.execute(sql)
            results = cursor.fetchall()

            fileName = './transcript_'+studentID+'.txt'

            name_fetch_sql = "SELECT First_Name, Last_Name FROM STUDENT WHERE Roll_No = '%s';" % (studentID)
            cursor.execute(name_fetch_sql)
            name_fetch_res = cursor.fetchall()
            firstName = name_fetch_res[0][0]
            lastName = name_fetch_res[0][1]

            firstLine = "Transcript of " + firstName + " " + lastName + "\n"
            secondLine = "Enrollment Number: "+studentID + "\n"
            thirdLine = "Batch of "+str(year) + "\n\n"

            with open(fileName, 'a') as f:
                f.write(firstLine)
                f.write(secondLine)
                f.write(thirdLine)
            
            res = tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql')
            with open(fileName, 'a') as f:
                printer = "Semester 1\n"
                f.write(printer)
                f.write(res)
                f.write("\n\n\n")


            print("\n\nFile Generated successfully. File Name: ", fileName)
            input("Press any key to continue.")

            return
    else:
        #year == 2021

        fileName = './transcript_'+studentID+'.txt'

        if os.path.exists(fileName):
            os.remove(fileName)

        name_fetch_sql = "SELECT First_Name, Last_Name FROM STUDENT WHERE Roll_No = '%s';" % (studentID)
        cursor.execute(name_fetch_sql)

        name_fetch_res = cursor.fetchall()
        firstName = name_fetch_res[0][0]
        lastName = name_fetch_res[0][1]

        firstLine = "Transcript of " + firstName + " " + lastName + "\n"
        secondLine = "Enrollment Number: "+studentID + "\n"
        thirdLine = "Batch of "+str(year) + "\n\n"

        with open(fileName, 'a') as f:
            f.write(firstLine)
            f.write(secondLine)
            f.write(thirdLine)


        for semester in range(1, 3):
            table_name = studentID+'_'+str(semester)

            sql = "SELECT * FROM %s;" % (table_name)

            cursor.execute(sql)

            results = cursor.fetchall()
            res = tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql')

            # res.to_csv('./transcript_'+studentID, header = None, sep = ' ', mode = 'w', index = None)
            # fileName = './transcript_'+studentID+'.txt'
            
            with open(fileName, 'a') as f:
                printer = "Semester "+ str(semester)+"\n"
                f.write(printer)
                f.write(res)
                f.write("\n\n\n")

        table_name = studentID+'_3'

        table_check_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (table_name)
        cursor.execute(table_check_sql)

        table_check_res = cursor.fetchall()

        if table_check_res[0][0] == 1:

            sql = "SELECT * FROM %s;" % (table_name)

            cursor.execute(sql)

            results = cursor.fetchall()
            res = tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql')


            with open(fileName, 'a') as f:
                printer = "Semester 3\n"
                f.write(printer)
                f.write(res)
                f.write("\n")

        fetch_sql = "SELECT Course_ID FROM COURSE_DROPPED WHERE Roll_No = '%s';" % (studentID)
        cursor.execute(fetch_sql)

        fetch_res = cursor.fetchall()

        # print(fetch_res)

        if fetch_res != []:
            printer = "\nWithdrawn Courses in Semester 3\n"
            with open(fileName, 'a') as f:
                f.write(printer)

            for val in fetch_res:
                fetch_course_det_sql = "SELECT Course_ID, Course_Title, C FROM COURSES WHERE Course_ID = '%s';" % (val[0])
                cursor.execute(fetch_course_det_sql)

                fetch_course_det_res = cursor.fetchall()

                res_ = tabulate(fetch_course_det_res, tablefmt='psql')

                with open(fileName, 'a') as f:
                    # f.write(printer)
                    f.write(res_)
                    f.write("\n")

            # for val in fetch_course_det_res:
            #     print(val, "W")



    print("\nFile Path: ", fileName)
    input("\nPress any key to continue.")
    return
            



    # if year == '2021' and current_year == 2022 and current_sem == 1:
    #     fileName = './transcript_'+studentID+'.txt'
    #     name_fetch_sql = "SELECT First_Name, Last_Name FROM STUDENT WHERE Roll_No = '%s';" % (studentID)
    #     cursor.execute(name_fetch_sql)
    #     name_fetch_res = cursor.fetchall()
    #     firstName = name_fetch_res[0][0]
    #     lastName = name_fetch_res[0][1]

    #     firstLine = "Transcript of " + firstName + " " + lastName + "\n"
    #     secondLine = "Enrollment Number: "+studentID + "\n"
    #     thirdLine = "Batch of "+str(year) + "\n\n"

    #     with open(fileName, 'a') as f:
    #         f.write(firstLine)
    #         f.write(secondLine)
    #         f.write(thirdLine)


    #     for semester in range(1, 3):
    #         table_name = studentID+'_'+str(semester)

    #         sql = "SELECT * FROM %s;" % (table_name)

    #         cursor.execute(sql)

    #         results = cursor.fetchall()
    #         res = tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql')

    #         # res.to_csv('./transcript_'+studentID, header = None, sep = ' ', mode = 'w', index = None)
    #         # fileName = './transcript_'+studentID+'.txt'
            
    #         with open(fileName, 'a') as f:
    #             printer = "Semester "+ str(semester)+"\n"
    #             f.write(printer)
    #             f.write(res)
    #             f.write("\n\n\n")


    #     print("\nFile Path: ", fileName)
    #     input("\nPress any key to continue.")

def viewGrades():
    click.clear()

    student_list_sql = "SELECT Roll_No, First_Name, Last_Name FROM STUDENT;"
    cursor.execute(student_list_sql)

    student_list_res = cursor.fetchall()

    print(tabulate(student_list_res, headers = ['Enrollment Number', 'First Name', 'Last Name'], tablefmt='psql'))

    studentID = input("Enter Student Enrollment Number: ")
    sem = input("Enter Semester of student: ")
    year = input("Enter Year in which student is studying: ")

    table_name = studentID+'_'+sem

    table_check_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (table_name)
    cursor.execute(table_check_sql)

    table_check_res = cursor.fetchall()

    if table_check_res[0][0] == 0:
        print("Gradesheet doesn't exist. Please try again with valid input.")
        input("Press any key to continue")

        return
    else:
        sql = "SELECT * FROM %s;" % (table_name)

        cursor.execute(sql)

        results = cursor.fetchall()

        print("******** Gradesheet of Year ", year, "and Semester ", sem, "********")
        
        print(tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql'))

        print("\n\n")
        input("Press any key to continue.")

        return

def createNewCourse():
    click.clear()
    courseID = input("Enter Course ID: ")
    courseTitle = input("Enter Course Title: ")
    L, T, P, S, C = input("Enter Lecture(L) Tutorial(T) Practical(P) Seminar(S) Credits(C): ").split(' ')
    c_preReq = list(input("Enter Course Pre-Req: (Enter NIL if no pre-requisites: ").split(' '))

    courses_sql = "INSERT INTO COURSES VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (str(courseID), str(courseTitle), str(L), str(T), str(P), str(S), str(C))
    # print(sql)
    cursor.execute(courses_sql)

    # print(c_preReq)

    for val in c_preReq:
        prereq_sql = "INSERT INTO COURSES_PREREQ VALUES ('%s', '%s');" % (courseID, val)
        cursor.execute(prereq_sql)

    db.commit()

    db.close()
    # time.sleep(2)
    print("Course Insertion Successful!")
    time.sleep(3)

def editCourseCatalog():
    click.clear()

    fetch_sql = "SELECT * FROM COURSES;"
    cursor.execute(fetch_sql)

    fetch_res = cursor.fetchall()

    print(tabulate(fetch_res, headers=['Course ID', 'Course Title', 'L', 'T', 'P', "S", 'C'], tablefmt='psql'))

    courseID = input("Enter Course ID whose data you want to edit: ")
    L, T, P, S, C = input("Enter Lecture(L) Tutorial(T) Practical(P) Seminar(S) Credits(C): (Enter NIL if no changes needed)").split(' ')

    if(L != 'NIL'):
        sql = "UPDATE COURSES SET L = '%s' WHERE Course_ID = '%s' ;" % (str(L), str(courseID))

        cursor.execute(sql)

        db.commit()

    elif(T != 'NIL'):
        sql = "UPDATE COURSES SET T = '%s' WHERE Course_ID = '%s' ;" % (str(T), str(courseID))

        cursor.execute(sql)

        db.commit()

    elif(P != 'NIL'):
        sql = "UPDATE COURSES SET P = '%s' WHERE Course_ID = '%s' ;" % (str(P), str(courseID))

        cursor.execute(sql)

        db.commit()

    elif(S != 'NIL'):
        sql = "UPDATE COURSES SET S = '%s' WHERE Course_ID = '%s' ;" % (str(S), str(courseID))

        cursor.execute(sql)

        db.commit()

    elif(C != 'NIL'):
        sql = "UPDATE COURSES SET C = '%s' WHERE Course_ID = '%s' ;" % (str(C), str(courseID))

        cursor.execute(sql)

        db.commit()

    db.close()
    # time.sleep(2)
    print("Course Updation Successful!")
    time.sleep(3)

def acadOfficeMenu(userID, current_sem, current_year):

    sql = "select First_Name, Last_Name from ACADOFFICE where UserID = '%s'" % (userID)
    cursor.execute(sql)

    results = cursor.fetchall()

    # print(results[0])

    while(1):
        click.clear()
        if results[0][1] != 'nan':
            print("********** Welcome ", results[0][0], results[0][1], " **********")
        else:
            print("********** Welcome ", results[0][0], " **********")
        print("1. Create a new Course")
        print("2. Edit Course Catalog")
        print("3. View Grades of all Students")
        print("4. Download Transcript")
        print("5. Logout")

        choice = input()

        if(choice == str(1)):
            createNewCourse()
        elif(choice == str(2)):
            if (userID == 'staffdeanoffice'):
                editCourseCatalog()
            else:
                print("You don't have access to this section. Please check the username with which you are trying to access Edit Course Catalog subsection.\nPlease try again!!!")
                time.sleep(3)
        elif(choice == str(3)):
            viewGrades()
        elif(choice == str(4)):
            downloadTranscript(current_sem, current_year)
        elif(choice == str(5)):
            logout(userID)
            return
        else:
            input("\n\nWrong Input. Please try again! \n Press any key to continue")

