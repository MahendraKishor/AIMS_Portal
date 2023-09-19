import random as r
import pandas as pd

data = pd.read_csv('./dataset/acadOfficeRecord.csv')


for i in range(data.shape[0]):
    ph_no = []
    
    # the first number should be in the range of 6 to 9
    ph_no.append(r.randint(6, 9))
    
    # the for loop is used to append the other 9 numbers.
    # the other 9 numbers can be in the range of 0 to 9.
    for i in range(1, 10):
        ph_no.append(r.randint(0, 9))
    
    # printing the number
    for i in ph_no:
        print(i, end = "")

    print("")

# for i in range(1, 38):
#     cgpa = round(random.uniform(6.5, 10), 2)
#     print(cgpa)