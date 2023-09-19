import mysql.connector
import studentMenuPage
import facultyMenuPage
import acadOfficeMenuPage
import click
import hashlib
import pwinput
import time
import datetime

salt = b'32'

db = mysql.connector.connect(host='localhost', user='root', password='password123', database = "PGLAB")
cursor = db.cursor()

userID = ""
password = ""



def login(userID, hashed_pass, current_sem, current_year):
    sql = "select * from LOGIN_RECORD where User_ID = '%s' and Password = '%s';" % (userID, hashed_pass)
    # print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()

    # print(results)
    # print(type(results[0][2]))
    if results == []:
        print("Incorrect User ID / Password. Please Try Again!")
        time.sleep(3)
        loginModule(current_sem, current_year)

    elif results[0][1] == hashed_pass:

        checker_sql = "SELECT EXISTS(SELECT * FROM SESSION WHERE User_ID = '%s');" % (userID)
        cursor.execute(checker_sql)

        checker_res = cursor.fetchall()

        if(checker_res[0][0] == 0):  #Means userID not present inside session table

            if results[0][2] == '1':
                ts = time.time()

                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                session_sql = "INSERT INTO SESSION VALUES ('%s', '%s', '%s');" % (userID, timestamp, results[0][2])

                cursor.execute(session_sql)
                db.commit()
                print("Login Successful. Redirecting...")

                time.sleep(1)

                acadOfficeMenuPage.acadOfficeMenu(userID, current_sem, current_year)

            elif results[0][2] == '2':
                ts = time.time()

                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                session_sql = "INSERT INTO SESSION VALUES ('%s', '%s', '%s');" % (userID, timestamp, results[0][2])

                cursor.execute(session_sql)
                db.commit()
                print("Login Successful. Redirecting...")

                time.sleep(1)

                facultyMenuPage.facultyMenu(userID, current_sem, current_year)

            elif results[0][2] == '3':
                ts = time.time()

                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                session_sql = "INSERT INTO SESSION VALUES ('%s', '%s', '%s');" % (userID, timestamp, results[0][2])

                cursor.execute(session_sql)
                db.commit()
                print("Login Successful. Redirecting...")
                time.sleep(1)
                studentMenuPage.studentMenu(userID, current_sem, current_year)
        else:
            print("You are already logged-in. Redirecting...")

            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            time.sleep(3)
            
            fetch_sql = "SELECT User_Type FROM SESSION WHERE User_ID = '%s'" % (userID)

            cursor.execute(fetch_sql)

            fetch_res = cursor.fetchall()

            if(fetch_res[0][0] == '1'):
                session_update_sql = "UPDATE SESSION SET Time = '%s' WHERE User_ID = '%s';" % (timestamp, userID)
                cursor.execute(session_update_sql)
                db.commit()
                acadOfficeMenuPage.acadOfficeMenu(userID, current_sem, current_year)
            elif (fetch_res[0][0] == '2'):
                session_update_sql = "UPDATE SESSION SET Time = '%s' WHERE User_ID = '%s';" % (timestamp, userID)
                cursor.execute(session_update_sql)
                db.commit()
                facultyMenuPage.facultyMenu(userID, current_sem, current_year)
            elif fetch_res[0][0] == '3':
                session_update_sql = "UPDATE SESSION SET Time = '%s' WHERE User_ID = '%s';" % (timestamp, userID)
                cursor.execute(session_update_sql)
                db.commit()
                studentMenuPage.studentMenu(userID, current_sem, current_year)
    

def loginModule(current_sem, current_year):
    click.clear()
    print("********** Login Page **********")
    userID = input("User ID: ")
    # print("Password: ")
    password = pwinput.pwinput()
    # print(password)
    # print("\n")
    password = password.encode()
    # print(password)
    hashed_pass = hashlib.sha512(password).hexdigest()
    # print(hashed_pass)

    login(userID, hashed_pass, current_sem, current_year)

# loginModule()