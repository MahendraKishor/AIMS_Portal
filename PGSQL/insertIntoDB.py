import pandas as pd
import mysql.connector
import csv
import hashlib

db = mysql.connector.connect(host='localhost', user='root', password='password123', database = "PGLAB")
cursor = db.cursor()
# db.autocommit(True)

f = open('./dataset/studentRecord.csv', 'w')

sql = "SELECT * FROM STUDENT;"

cursor.execute(sql)
writer = csv.writer(f)
writer.writerow(['First_Name', 'Last_Name', 'Roll_No', 'EmailID', 'Contact', 'CGPA', 'Sem', 'Year'])

res = cursor.fetchall()

for val in res:
    writer.writerow(val)
#Gradesheet

# df = pd.read_csv('./dataset/2021CSM1003_1.csv')
# total_points = 0

# # sql_header = 

# for val in df.values:
#     courseID = val[0]
#     courseTitle = val[1]
#     credit = val[2]
#     grade = val[3]

#     sql = "INSERT INTO 2021CSM1003_1 VALUES ('%s', '%s', '%s', '%s');" % (courseID, courseTitle, credit, grade)

#     cursor.execute(sql)

#     db.commit()


#     my_dict = {
#         'A' : 10,
#         'A-' : 9,
#         'B' : 8,
#         'B-' : 7,
#         'C' : 6,
#         'D' : 5
#     }


#     total_points += my_dict[grade]

# cgpa = round(total_points / 4, 2)





#Student Handling

# df = pd.read_csv('./dataset/studentRecord.csv')

# # print(df.shape[0])
# f = open('./dataset/loginRecord.csv', 'a')
# writer = csv.writer(f)
# # writer.writerow(['User_ID', 'Password', 'User_Type'])

# for val in df.values:
#     rno = str(val[2])
#     mob = str(val[4])

#     mob = mob.encode()

#     hashed_pass = hashlib.sha512(mob).hexdigest()
#     # print(rno, hashed_pass)
#     writer.writerow([rno, hashed_pass, 3])

# with open('./dataset/loginRecord.csv') as file_obj:
      
#     # Skips the heading
#     # Using next() method
#     heading = next(file_obj)
      
#     # Create reader object by passing the file 
#     # object to reader method
#     reader_obj = csv.reader(file_obj)
      
#     # Iterate over each row in the csv file 
#     # using reader object
#     for row in reader_obj:
#         # print(row)
#         # sql = "insert into LOGIN_RECORD (User_ID, Password, User_Type) VALUES (?, ?, ?);"
#         # print(sql, tuple(row))
#         sql = "INSERT INTO LOGIN_RECORD VALUES ('%s', '%s', '%s');" % (str(row[0]), str(row[1]), str(row[2]))
#         # print(sql)
#         cursor.execute(sql)
#         db.commit()

# db.close()

# Faculty Handling

# df = pd.read_csv('./dataset/studentRecord.csv')

# # print(df.shape[0])
# f = open('./dataset/loginRecord.csv', 'a')
# writer = csv.writer(f)
# # writer.writerow(['User_ID', 'Password', 'User_Type'])

# for val in df.values:
#     f_id = str(val[2])
#     mob = str(val[4])

#     mob = mob.encode()

#     hashed_pass = hashlib.sha512(mob).hexdigest()
#     # print(rno, hashed_pass)
#     writer.writerow([f_id, hashed_pass, 3])

# with open('./dataset/loginRecord.csv') as file_obj:
      
#     # Skips the heading
#     # Using next() method
#     heading = next(file_obj)
      
#     # Create reader object by passing the file 
#     # object to reader method
#     reader_obj = csv.reader(file_obj)
      
#     # Iterate over each row in the csv file 
#     # using reader object
#     for row in reader_obj:
#         # print(row)
#         # sql = "insert into LOGIN_RECORD (User_ID, Password, User_Type) VALUES (?, ?, ?);"
#         # print(sql, tuple(row))
#         sql = "INSERT INTO LOGIN_RECORD VALUES ('%s', '%s', '%s');" % (str(row[0]), str(row[1]), str(row[2]))
#         # print(sql)
#         cursor.execute(sql)
#         db.commit()

# db.close()

# with open('./dataset/coursePreReq.csv') as file_obj:
      
#     # Skips the heading
#     # Using next() method
#     heading = next(file_obj)
      
#     # Create reader object by passing the file 
#     # object to reader method
#     reader_obj = csv.reader(file_obj)
      
#     # Iterate over each row in the csv file 
#     # using reader object
#     for row in reader_obj:
#         # print(row)
#         # sql = "insert into LOGIN_RECORD (User_ID, Password, User_Type) VALUES (?, ?, ?);"
#         # print(sql, tuple(row))
#         # pre_req1, pre_req2 = str(row[7]).split(',')
#         sql = "INSERT INTO COURSES_PREREQ VALUES ('%s', '%s');" % (str(row[0]), str(row[1]))
#         # print(sql)
#         cursor.execute(sql)
#         db.commit()

# db.close()

# with open('./dataset/courses.csv') as file_obj:
      
#     # Skips the heading
#     # Using next() method
#     heading = next(file_obj)
      
#     # Create reader object by passing the file 
#     # object to reader method
#     reader_obj = csv.reader(file_obj)
      
#     # Iterate over each row in the csv file 
#     # using reader object
#     for row in reader_obj:
#         # print(row)
#         # sql = "insert into LOGIN_RECORD (User_ID, Password, User_Type) VALUES (?, ?, ?);"
#         # print(sql, tuple(row))

#         sql = "INSERT INTO COURSES VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]))
#         # print(sql)
#         cursor.execute(sql)
#         db.commit()

# db.close()


# with open('./dataset/studentRecord.csv') as file_obj:
      
#     # Skips the heading
#     # Using next() method
#     heading = next(file_obj)
      
#     # Create reader object by passing the file 
#     # object to reader method
#     reader_obj = csv.reader(file_obj)
      
#     # Iterate over each row in the csv file 
#     # using reader object
#     for row in reader_obj:
#         sql = "insert into STUDENT (First_Name, Last_Name, Roll_No, EmailID, Contact, CGPA) VALUES (?, ?, ?, ?, ?, ?);"
#         cursor.execute(sql, tuple(row))
#print(df)
#print(df[2])
#print(df[3])

# import numpy as np
# np.isnan(df)


# df = pd.read_csv('./dataset/studentRecord.csv')

# for val in df.values:
#     fname = str(val[0])
#     lname = str(val[1])
#     rno = str(val[2])
#     email = str(val[3])
#     mob = str(val[4])
#     cgpa = str(val[5])   
#     # print(fname, lname, rno, email, mob, cgpa)
#     # sql = "INSERT INTO STUDENT VALUES (%s, %s, %s, %s, %s, %s);", (fname, lname, rno, email, mob, cgpa)
#     sql = "INSERT IGNORE INTO STUDENT VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (str(fname), str(lname), str(rno), str(email), str(mob), str(cgpa), str(val[6]), str(val[7]))
#     # print(sql)
#     # cursor.execute(sql, (str(fname), str(lname), str(rno), str(email), str(mob), str(cgpa)))
#     cursor.execute(sql)
#     db.commit()

# db.close()

# df = pd.read_csv('./dataset/acadOfficeRecord.csv')

# for val in df.values:
#     fname = str(val[0])
#     lname = str(val[1])
#     fid = str(val[2])
#     email = str(val[3])
#     mob = str(val[4])  
#     # print(fname, lname, rno, email, mob, cgpa)
#     # sql = "INSERT INTO STUDENT VALUES (%s, %s, %s, %s, %s, %s);", (fname, lname, rno, email, mob, cgpa)
#     sql = "INSERT INTO ACADOFFICE VALUES ('%s', '%s', '%s', '%s', '%s');" % (str(fname), str(lname), str(fid), str(email), str(mob))
#     # print(sql)
#     # cursor.execute(sql, (str(fname), str(lname), str(rno), str(email), str(mob), str(cgpa)))
#     cursor.execute(sql)
#     db.commit()

# db.close()

# for val in df.values:
#     sql = "insert into STUDENT VALUES ({0}, {1}, {2}, {3}, {4}, {5})".format(str(val[0]), str(val[1]), str(val[2]), str(val[3]), str(val[4]), str(val[5]))
#     cursor.execute(sql)
# for index, row in df.iterrows():
#     print(row)

# for index, row in df.iterrows():
#     cursor.execute('INSERT INTO STUDENTS ([First_Name], [Last_Name], [Roll_No], [EmailID], [Contact], [CGPA]) VALUES (?, ?, ?, ?, ?, ?)', row)

# for val in df.values:
#     fname = val[0]
#     lname = val[1]
#     rno = val[2]

# df = pd.read_csv('./dataset/studentRecord.csv')

# for val in df.values:
#     rollNo = str(val[2])
#     sem = str(val[6])
#     year = str(val[7])

#     fileName = rollNo+'_'+sem

#     print(fileName)