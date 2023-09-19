import click
import mysql.connector
import pandas as pd
import time
from tabulate import tabulate

db = mysql.connector.connect(host='localhost', user='root', password='password123', database = "PGLAB")
cursor = db.cursor()

def viewCGPA(rollNo):
    click.clear()
    l_year = rollNo
    
    year = l_year[0] + l_year[1] + l_year[2] + l_year[3]

    if year == '2022':
        print("You cannot view your CGPA before semester completion.")
        print("Redirecting...")

        time.sleep(3)
        return

    else:
        sem = input("Enter Semester: ")
        if(int(sem) > 2):
            print("You cannot view your CGPA before semester completion.")
            print("Redirecting...")

            time.sleep(3)
            return

        table_name = rollNo+'_'+sem

        sql = "SELECT * FROM %s;" % (table_name)

        cursor.execute(sql)

        results = cursor.fetchall()

        my_dict = {
            'A' : 10,
            'A-' : 9,
            'B' : 8,
            'B-' : 7,
            'C' : 6,
            'D' : 5,
            'F' : 0
        }

        total_cgpa = 0
        for val in results:
            # print(my_dict[val[3]])
            total_cgpa += my_dict[val[3]]

        print("Your CGPA for semester ", sem, " is ", round((total_cgpa / 4.0), 2))

        print("\n")
        input("Press any key to continue.")

        

def viewGrades(rollNo):
    click.clear()
    l_year = rollNo
    
    year = l_year[0] + l_year[1] + l_year[2] + l_year[3]

    if year == '2022':
        fileName = rollNo + '_1'
        table_check_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (fileName)
        cursor.execute(table_check_sql)

        table_check_res = cursor.fetchall()

        if table_check_res[0][0] == 0:
            print("\nYour grades are not entered yet. Please try again later.")
            input("\n\nPress any key to continue")
            return
        else:
            sql = "SELECT * FROM %s;" % (fileName)
            cursor.execute(sql)

            results = cursor.fetchall()

            print("******** Gradesheet of Year ", year, "and Semester 1 ********")
            
            print(tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql'))

            print("\n\n")
            input("Press any key to continue.")

        return

    else:
        sem = input("Enter Semester: ")
        fileName = rollNo + '_' + str(sem)
        
        table_check_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (fileName)
        cursor.execute(table_check_sql)

        table_check_res = cursor.fetchall()

        if table_check_res[0][0] == 0:
            print("\nYour grades are not entered yet. Please try again later.")
            input("\n\nPress any key to continue")
            return
        else:
            sql = "SELECT * FROM %s;" % (fileName)
            cursor.execute(sql)

            results = cursor.fetchall()

            print("******** Gradesheet of Year ", year, "and Semester ", sem, "********")
            
            print(tabulate(results, headers=['Course_ID', 'Course_Title', 'Credits', 'Grade'], tablefmt='psql'))

            print("\n\n")
            input("Press any key to continue.")

        return

def registerForCourse(rollNo):
    click.clear()
    fetch_sql = "SELECT Sem, Year FROM STUDENT WHERE Roll_No = '%s';" % (rollNo)

    cursor.execute(fetch_sql)

    fetch_res = cursor.fetchall()

    if(fetch_res[0][0] == '1' and fetch_res[0][1] == '2022'):
        # click.clear()
        print("CS506\nCS509\nCS526\nCS527\nThese are core courses and are already registered for you. \nRedirecting to home page...")

        time.sleep(5)
    else: # either sem 2 of year 2022 or 2021 batch sem 3
        fetch_from_courses = "SELECT FacultyID, COURSES_OFFERED.Course_ID, Course_Title, L, T, P, S, C, CGPA_Constraint FROM COURSES_OFFERED INNER JOIN COURSES ON COURSES_OFFERED.Course_ID = COURSES.Course_ID;"

        cursor.execute(fetch_from_courses)

        courses_offered_result = cursor.fetchall()
        # df = pd.DataFrame()

        # print(courses_offered_result[1])
        # print(courses_offered_result)
        pre_req_list = dict()


        for val in courses_offered_result:

            fetch_pre_req = "SELECT Course_ID, Pre_Req FROM COURSES_PREREQ WHERE Course_ID = '%s'" % (val[1])

            cursor.execute(fetch_pre_req)

            pre_req_res = cursor.fetchall()

            
            for item in pre_req_res:
                pre_req_list[item[0]] = []

            for key in pre_req_list:
                # print(key)
                for val in pre_req_res:

                    if(key == val[0]):
                        pre_req_list[key].append(val[1])
                

        # print(pre_req_list)

        # for key in pre_req_list.keys():
        #     print(key)

        
        df = pd.DataFrame(courses_offered_result, columns = ['Faculty ID', 'Course ID', 'Course Title', 'L', 'T', 'P', 'S', 'C', 'CGPA Constraint'])
        # df.reset_index(drop = True)

        # for val in df['Course_ID']:
        #     print(pre_req_list[val])


        df['Pre Requisites'] = [pre_req_list[val] for val in df['Course ID']]
        print(df)
        
        print("\n\n")
        courseID = input("Enter Course ID you want to register: ")

        checker_sql = "SELECT EXISTS(SELECT * FROM COURSE_REGD WHERE Course_ID = '%s' AND Roll_No = '%s');" % (courseID, rollNo)
        cursor.execute(checker_sql)
        checker_res = cursor.fetchall()

        if checker_res[0][0] == 1:
            print("You have already registered for this course.")
            input("Press any key to continue.")
            return

        lst = []

        for semester in range(1, 3):
            fileName = rollNo + '_' + str(semester)
            courseID_check_sql = "SELECT Course_ID, Grade FROM %s" % (fileName)
            cursor.execute(courseID_check_sql)
            courseID_check_res = cursor.fetchall()

            for val in courseID_check_res:
                if courseID in val[0] and val[1] != 'F':
                    print("You have already completed this course. Can't re-register.")

                    input("Press any key to continue.")
                    return


        dereg_fetch_sql = "SELECT EXISTS(SELECT * FROM COURSE_DROPPED WHERE Course_ID = '%s' AND Roll_No = '%s')" % (courseID, rollNo)
        cursor.execute(dereg_fetch_sql)
        dereg_fetch_res = cursor.fetchall()

        if(dereg_fetch_res == []):

            credit_fetch_sql = "SELECT C FROM COURSES WHERE Course_ID = '%s';" % (courseID)
            cursor.execute(credit_fetch_sql)
            credit_fetch_res = cursor.fetchall()

            if credit_fetch_res != []:
                this_course_credit = int(credit_fetch_res[0][0])

            if courseID not in pre_req_list.keys():
                print("\n\nPlease enter a course that is in Course Offered List. ")
                input("\n\nPress any key to continue")
                return
            else:

                fetch_cgpa = "SELECT CGPA FROM STUDENT WHERE Roll_No = '%s';" % (rollNo)

                cursor.execute(fetch_cgpa)

                res_cgpa = cursor.fetchall()

                cgpa = res_cgpa[0][0]

                # print(cgpa)

                cgpa_fetch_faculty = "SELECT CGPA_Constraint FROM COURSES_OFFERED WHERE Course_ID = '%s';" % (courseID)
                cursor.execute(cgpa_fetch_faculty)

                res_cgpa_faculty = cursor.fetchall()

                CGPA_Constraint_ = res_cgpa_faculty[0][0]
                
                if float(cgpa) < float(CGPA_Constraint_):
                    print("Minimum CGPA Criteria for this course is not satisfied.\nYour: ",cgpa,"\nRequired: ",CGPA_Constraint_)
                else:
                    courseList = []
                    creditSum = 0
                    for i in range(1, 3):
                        table_name = rollNo + '_' + str(i)
                        fetch_student_prereq_sem = "SELECT Course_ID, Credits, Grade FROM %s;" % (table_name)
                        cursor.execute(fetch_student_prereq_sem)

                        fetched_res = cursor.fetchall()
                        
                        for val in fetched_res:
                            courseList.append(val[0])
                            if val[2] != 'F':
                                creditSum += int(val[1])

                    # print(courseList)
                    # print(creditSum)

                    for preReq in pre_req_list[courseID]:
                        if preReq == 'NIL':
                            break
                        if preReq not in courseList:
                            print("You do not Satisfy the Course Pre Requisites. Please register in another course.")
                            input("Press any key to continue")

                            return

                    # Means pre reqs are satisfied
                    total_credits_allowed = 1.25 * (creditSum / 2.0)

                    courses_regd_sql = "SELECT Credits FROM COURSE_REGD WHERE Roll_No = '%s';" % (rollNo)
                    cursor.execute(courses_regd_sql)

                    courses_regd_res = cursor.fetchall()

                    # print(courses_regd_res)


                    credit_res = 0

                    if courses_regd_res != []:
                        for i in courses_regd_res[0]:
                            credit_res += int(i)

                    if total_credits_allowed - this_course_credit - credit_res < 0:
                        print("You have already exceeded the allowed credits for this semester. Please drop a course to enroll this course.")
                        print("\n\n")
                        input("Press any key to continue")
                        return
                    else:
                        insert_into_course_regd_sql = "INSERT INTO COURSE_REGD VALUES('%s', '%s', '%s');" % (rollNo, courseID, str(this_course_credit))
                        cursor.execute(insert_into_course_regd_sql)
                        db.commit()

                        print("You have successfully registered for ", courseID) 

                input("Press any key to continue")
        else:
            # print("\n\nCannot re-register for this course, as you have previously registered the course and then dropped it.")

            # input("\nPress any key to continue.")

            delete_sql = "DELETE FROM COURSE_DROPPED WHERE Course_ID = '%s' and Roll_No = '%s';" % (courseID, rollNo)
            cursor.execute(delete_sql)

            credit_fetch_sql = "SELECT C FROM COURSES WHERE Course_ID = '%s';" % (courseID)
            cursor.execute(credit_fetch_sql)
            credit_fetch_res = cursor.fetchall()

            if credit_fetch_res != []:
                this_course_credit = int(credit_fetch_res[0][0])

            if courseID not in pre_req_list.keys():
                print("\n\nPlease enter a course that is in Course Offered List. ")
                input("\n\nPress any key to continue")
                return
            else:

                fetch_cgpa = "SELECT CGPA FROM STUDENT WHERE Roll_No = '%s';" % (rollNo)

                cursor.execute(fetch_cgpa)

                res_cgpa = cursor.fetchall()

                cgpa = res_cgpa[0][0]

                # print(cgpa)

                cgpa_fetch_faculty = "SELECT CGPA_Constraint FROM COURSES_OFFERED WHERE Course_ID = '%s';" % (courseID)
                cursor.execute(cgpa_fetch_faculty)

                res_cgpa_faculty = cursor.fetchall()

                CGPA_Constraint_ = res_cgpa_faculty[0][0]
                
                if float(cgpa) < float(CGPA_Constraint_):
                    print("Minimum CGPA Criteria for this course is not satisfied.\nYour: ",cgpa,"\nRequired: ",CGPA_Constraint_)
                else:
                    courseList = []
                    creditSum = 0
                    for i in range(1, 3):
                        table_name = rollNo + '_' + str(i)
                        fetch_student_prereq_sem = "SELECT Course_ID, Credits, Grade FROM %s;" % (table_name)
                        cursor.execute(fetch_student_prereq_sem)

                        fetched_res = cursor.fetchall()
                        
                        for val in fetched_res:
                            courseList.append(val[0])
                            if val[2] != 'F':
                                creditSum += int(val[1])

                    # print(courseList)
                    # print(creditSum)

                    for preReq in pre_req_list[courseID]:
                        if preReq == 'NIL':
                            break
                        if preReq not in courseList:
                            print("You do not Satisfy the Course Pre Requisites. Please register in another course.")
                            input("Press any key to continue")

                            return

                    # Means pre reqs are satisfied
                    total_credits_allowed = 1.25 * (creditSum / 2.0)

                    courses_regd_sql = "SELECT Credits FROM COURSE_REGD WHERE Roll_No = '%s';" % (rollNo)
                    cursor.execute(courses_regd_sql)

                    courses_regd_res = cursor.fetchall()

                    # print(courses_regd_res)


                    credit_res = 0

                    if courses_regd_res != []:
                        for i in courses_regd_res[0]:
                            credit_res += int(i)

                    if total_credits_allowed - this_course_credit - credit_res < 0:
                        print("You have already exceeded the allowed credits for this semester. Please drop a course to enroll this course.")
                        print("\n\n")
                        input("Press any key to continue")
                        return
                    else:
                        insert_into_course_regd_sql = "INSERT INTO COURSE_REGD VALUES('%s', '%s', '%s');" % (rollNo, courseID, str(this_course_credit))
                        cursor.execute(insert_into_course_regd_sql)
                        db.commit()

                        print("You have successfully registered for ", courseID) 

                input("Press any key to continue")

            


def deregisterForCourse(rollNo):

    l_year = rollNo
    
    year = l_year[0] + l_year[1] + l_year[2] + l_year[3]

    if year == '2022':
        print("\nYou are not allowed to de-register any core courses.")
        input("\n\nPress any key to continue.")

        return

    click.clear()

    fetch_sql = "SELECT * FROM COURSE_REGD WHERE Roll_No = '%s';" % (rollNo)
    cursor.execute(fetch_sql)

    fetch_res = cursor.fetchall()

    if(fetch_res == []):
        print("You dont have any registed courses.")
        input("\n\nPress any key to continue")
        return

    print("\n\n********** Registered Courses **********")

    print(tabulate(fetch_res, headers=['Roll No', 'Course ID', 'Credits'], tablefmt='psql'))

    courseID = input("\n\nEnter Course ID to drop: ")

    course_detail_sql = "SELECT Roll_No, Course_ID FROM COURSE_REGD WHERE Course_ID = '%s'" % (courseID)
    cursor.execute(course_detail_sql)

    course_detail_res = cursor.fetchall()

    push_into_drop_table_sql = "INSERT INTO COURSE_DROPPED VALUES ('%s', '%s');" % (course_detail_res[0][0], course_detail_res[0][1])
    cursor.execute(push_into_drop_table_sql)
    
    table_checker_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'PGLAB') AND (TABLE_NAME = '%s');" % (courseID)
    cursor.execute(table_checker_sql)

    table_checker_res = cursor.fetchall()
    if table_checker_res[0][0] == 1:
        delete_from_course_sql = "DELETE FROM %s WHERE Roll_No = '%s';" % (courseID, rollNo)
        cursor.execute(delete_from_course_sql)


    # print(courseID)
    delete_from_regd_sql = "DELETE FROM COURSE_REGD WHERE Course_ID = '%s' AND Roll_No = '%s'" % (courseID, rollNo)
    cursor.execute(delete_from_regd_sql) 

    db.commit()

    print("\nCourse Successfully De-Registered.")


    input("\n\nPress any key to continue")


def logout(userID):
    sql = "DELETE FROM SESSION WHERE User_ID = '%s';" % (userID)
    cursor.execute(sql)
    db.commit()
    click.clear()

def studentMenu(rollNo, current_sem, current_year):

    sql = "select First_Name, Last_Name from STUDENT where Roll_No = '%s'" % (rollNo)
    cursor.execute(sql)

    results = cursor.fetchall()

    # print(results[0])

    while(1):
        click.clear()
        if results[0][1] != 'nan':
            print("********** Welcome ", results[0][0], results[0][1], " **********")
        else:
            print("********** Welcome ", results[0][0], " **********")
        print("1. View Grade Sheet")
        print("2. View CGPA")
        print("3. Register for a course")
        print("4. De-register a course")
        print("5. Logout")

        choice = input()

        if(choice == str(1)):
            viewGrades(rollNo)
        elif(choice == str(2)):
            viewCGPA(rollNo)
        elif(choice == str(3)):
            registerForCourse(rollNo)
        elif(choice == str(4)):
            deregisterForCourse(rollNo)
        elif(choice == str(5)):
            logout(rollNo)
            return
        else:
            input("\n\nWrong Input. Please try again! \n Press any key to continue")

