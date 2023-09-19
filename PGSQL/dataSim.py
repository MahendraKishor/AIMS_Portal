import pandas as pd
import csv
import random


#columns = [CourseID, Credits, Grade, Sem]
CourseID = ['CS506', 'CS509', 'CS526', 'CS527']
#CourseID = [CS503, CS504, CS507, CS512, CS517, CS518, CS521, CS522, CS524, CS530, CS532, CS533, CS535,CS539, CS545, CS612, CS617, CS621, CS615, CS623, CS720, CS724, CS546]
Credits = [3,4]
Grade = ['A', 'B', 'C', 'D', 'F']

list2 = []
for i in range(4):
    k={}
    courseID = random.choice(CourseID)
    credit = random.choice(Credits)
    grade = random.choice(Grade)
    k = {'CourseID': courseID, 'Credits': credit, 'Grade': grade}
    list2.append(k)

data = pd.DataFrame(list2)

print(data.head(5))